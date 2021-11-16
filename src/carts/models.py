from decimal import Decimal
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed

# Create your models here.
from products.models import Product
from products.models import Variation


User = settings.AUTH_USER_MODEL


# PRESENTATION = (
#             ('unidad', 'la unidad'),
#             ('peso', 'Kilo'),
#         )


class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE)
    item = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    presentation = models.CharField(max_length=120, default='unidad')
    line_item_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.item.title  # variation title coming through

    def get_quantity(self):
        return "{}".format(self.quantity)

    def remove(self):
        return self.item.remove_from_cart()

    def get_absolute_url(self):
        return "products/{pk}".format(pk=self.item.id)


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) > 0:
        price = instance.item.get_price()
        line_item_total = Decimal(qty) * Decimal(price)
        instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    items = models.ManyToManyField(Variation, through=CartItem)
    subtotal = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    tax_total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    cart_total = models.DecimalField(
        default=0.00, max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(
        default=0.13, max_digits=10, decimal_places=5)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal = 0
        items = self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

    def change_payment_method_url(self):
        return reverse('create_payment_method')

    @property
    def is_digital(self):
        qs = self.products.all()
        print
        new_qs = qs.filter(is_digital=True)
        if new_qs.exists():
            print("digital")
            return True
        print("not Digital")
        return False


def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    subtotal = instance.subtotal
    # costa rican sales tax
    tax_total = round(Decimal(subtotal) * Decimal(instance.tax_percentage), 2)
    cart_total = round(Decimal(subtotal) + tax_total, 2)
    instance.tax_total = tax_total
    instance.cart_total = round(cart_total, 2)
    # instance.save()  using pre_save this is not neccessary


pre_save.connect(do_tax_and_total_receiver, sender=Cart)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(instance)

        # cart.cartitem_set.first.quantity

        products = instance.products.all()
        cart_items = CartItem.objects.all()
        variation = Variation.objects.all()

        total = 0
        another_total = 0
        for x in products:
            # print("product", x, "price", x.price)

            var_name = x.variation_set.first()
            var_price = x.variation_set.first().get_price()

            cart_item = CartItem.objects.all().filter(item=var_name)
            qty = cart_item.values_list('quantity', flat=True)
            # qty = cart_item.values('quantity', flat=True)
            # print(var_name, "var_price", var_price, "cart_item", cart_item, " qty", qty)
            # qun = CartItem.objects.all().filter(item=var_name).get("quantity")

            # another_total += var_price * qty
            # print(type(another_total))

            total += x.price  # * x.qty
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = float(instance.subtotal) * float(1.08)
    else:
        instance.subtotal = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
