import json
from django.contrib.auth.forms import AuthenticationForm
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.core.mail import EmailMessage
from ecommerce.utils import render_to_pdf
from django.views.generic.base import View
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import SingleObjectMixin, DetailView

from decimal import Decimal

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm

from orders.forms import GuestCheckoutForm
# from orders.models import UserCheckout
from django.views.generic.edit import FormMixin

from .models import Cart, CartItem # CartItem experimental
from orders.models import Order
from accounts.models import GuestEmail
from products.models import Product, Variation  #### experimental Variation
from billing.models import BillingProfile
from addresses.models import Address


# Create your views here.
import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", 'sk_test_26VJVjIjh488Kcg0HRc5H4n3')
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", 'pk_test_6bFxudchtJMGKmlRu1EsOzJz')
stripe.api_key = STRIPE_SECRET_KEY


class CartItemsList(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id is not None:
                cart = Cart.objects.get(id=cart_id)
                cart_items = CartItem.objects.all().filter(cart=cart)
                items_in_cart = {}
                product_item = ""
                products = dict()
                if cart_items.count() > 0:
                    for items in cart_items:
                        item = str(items)
                        product_item = Product.objects.get(variation__title=item)
                        product = product_item.title
                        item_key = item.replace(" ", "_")
                        # items_in_cart[str(item_key)]["variation"] = item
                        items_in_cart[item] = str(items.quantity)
                        # items_in_cart[item]["presentation"] = str(items.presentation)
                        # print("Presentation ", presentation, ", item ", items)
                        products[item] = product
                else:
                    items_in_cart = {}
                request.session["items_cart"] = items_in_cart
                return JsonResponse({"items_cart": items_in_cart, "products": products})
            else:
                items_in_cart = None
        request.session["items_cart"] = items_in_cart
        return JsonResponse({"items_cart": items_in_cart})


class ItemCountView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404


# class to manage the cart, experimental, see ecommerce.urls
class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/view.html"
    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def post(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.POST.get("item")
        delete_item = request.POST.get("delete", False)
        item_added = False

        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            qty_ = request.POST.get("qty", 1)
            qty = Decimal(qty_)
            try:
                if qty <= 0:
                    delete_item = True
            except:
                print("getting this error")
                raise Http404

            if item_instance.inventory < qty:
                print("Out of stock")
                stock = 0
            else:
                cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
                if created:
                    item_added = True
                if delete_item:
                    cart_item.delete()
                else:
                    cart_item.quantity = qty

                    if item_instance.sale_price:
                        cart_item.line_item_total = qty * item_instance.sale_price
                    else:
                        cart_item.line_item_total = qty * item_instance.price

                    cart_item.presentation = item_instance.get_presentation()
                    # item_instance.inventory = item_instance.inventory - qty
                    item_instance.save()
                    cart_item.save()
                if not request.is_ajax():
                    return HttpResponseRedirect(reverse("cart-cbv"))
                if request.is_ajax():
                    try:
                        items_stock = stock
                    except:
                        items_stock = None
                    try:
                        item = cart_item.item.title
                        item_qty = str(qty)
                    except:
                        item = None
                    try:
                        total = cart_item.line_item_total
                    except:
                        total = None
                    try:
                        subtotal = cart_item.cart.subtotal
                    except:
                        subtotal = None
                    try:
                        cart_total = cart_item.cart.cart_total
                    except:
                        cart_total = None
                    try:
                        tax_total = cart_item.cart.tax_total
                    except:
                        tax_total = None
                    try:
                        total_items = cart_item.cart.items.count()
                    except:
                        total_items = 0

                    data = {
                        "item": item,
                        "item_qty": item_qty,
                        "deleted": delete_item,
                        "item_added": item_added,
                        "line_total": total,
                        "subtotal": subtotal,
                        "cart_total": cart_total,
                        "tax_total": tax_total,
                        "total_items": total_items,
                        "items_stock": items_stock,
                    }
                    return JsonResponse(data)

        context = {
                "object": self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        context = {
                "object": self.get_object(),
        }
        template = self.template_name
        return render(request, template, context)



# This is being used when products are deleted from cart
def cart_detail_api_view(request):
    print("old api cart total checkout******************")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name,
            "price": x.price,
            # "qty": x.qty  # *******quantity for the boostrap card component
            }
            for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)
#
def cart_home(request):
    print("Calling ")
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # cart_item, new_cart_item = CartItem.objects.
    # print("cart", cart_obj)
    return render(request, "carts/home.html", {'cart': cart_obj})


# question = get_object_or_404(Question, pk=question_id)
# try:
# selected_choice = question.choice_set.get(pk=request.POST['choice'])


#
# def cart_update(request):
#         # return JsonResponse({"message":"Error 400"}, status_code=400)
#     print("Old cart update**********delete")
#
#     product_id = request.POST.get('product_id')
#     item_id = request.POST.get("item")
#     qty = request.POST.get("product_qty")
#     if product_id is not None:
#         try:
#             product_obj = Product.objects.get(id=product_id)
#             item_instance = product_obj.variation_set.first()
#         except Product.DoesNotExist:
#             # print("Show message to the user, product is gone")
#             return redirect("cart:home")
#         cart_obj, new_obj = Cart.objects.new_or_get(request)
#         cart_item = CartItem.objects.get_or_create(cart=cart_obj, item=item_instance)[0]
#         # print(cart_obj)
#         # print(cart_item)
#         # print(request)
#         if product_obj in cart_obj.products.all():
#             cart_item.delete()
#             cart_obj.products.remove(product_obj)
#             added = False
#         else:
#             cart_item.quantity = qty
#             cart_obj.products.add(product_obj)
#             cart_item.save()
#             # cart_obj.cartitem.add(cart_item)  Trying to add cartitem to cart
#             # print("cart_item", cart_item, "  qty ", cart_item.quantity)
#             added = True
#         request.session['cart_items'] = cart_obj.products.count()
#         # print(request.session['cart_items'])
#         if request.is_ajax():
#             print("ajax request for products")
#             json_data = {
#             "added": added,
#             "removed": not added,
#             "cartItemCount": cart_obj.products.count(),
#             }
#             return JsonResponse(json_data, status=200)
#
#     return redirect("cart:home")



class CheckoutView(FormMixin, DetailView):
    model = Cart
    template_name = "carts/checkout_view.html"
    form_class = GuestCheckoutForm


    def get_object(self, *args, **kwargs):
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            return redirect("cart-cbv")
        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        if not self.request.user.is_authenticated(): # or request.user.is_guest:
            context['login_form'] = AuthenticationForm()
            context['next_url'] = self.request.build_absolute_uri()
        if self.request.user.is_authenticated():
            user_can_continue = True
        context['user_can_continue'] = user_can_continue
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            # user_checkout = UserCheckout.objects.create(email=email)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    variation = cart_obj.items.count()
    variation_all = cart_obj.items.all()

    # for item in cart_dict:
    #     print("\n\n****************************************cart_dict ", cart_dict)


    # if cart_created or cart_obj.products.count() == 0:
    if cart_created or cart_obj.items.count() == 0:
        return redirect("cart-cbv")
        # return redirect("cart-cbv:home")

    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressForm()

    shipping_address_id = request.session.get('shipping_address_id', None)
    # billing_address_id = shipping_address_id
    # billing_address_id = request.session.get('billing_address_id', None)
    # shipping_address_required = not cart_obj.is_digital

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    payment_method = None
    message = ''
    error = False

    payment_choices = {'efectivo': 'efectivo', 'tarjeta': 'tarjeta', 'paypal': 'PayPal'}

    if billing_profile is not None:
        # if request.user.is_authenticated():
        address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        "some check that order is done"
        is_prepared = order_obj.check_done()
        ready = False
        amount = request.POST.get('amount', None)

        if order_obj.payment_method:
            if order_obj.payment_method == 'tarjeta':
                ready = True

            if amount is not None and amount != '' and order_obj.payment_method == 'efectivo':
                amount = Decimal(amount)
                order_obj.cash_amount = amount
                order_obj.cash_process()
                if order_obj.cash_process() == False:
                    message = "Introduzca la cantidad correcta"
                    ready = False
                    error = True
                else:
                    ready = True
            else:
                error = True
                message = "Introduzca la cantidad correcta"

        if is_prepared and ready:
            did_charge, crg_msg = billing_profile.charge(order_obj)


            for var in variation_all:
                item = CartItem.objects.get(cart=cart_obj, item=var)
                print("***********variation ", var, " ", var.inventory)
                print(item.item.title, type(var))
                print(item.quantity)
                inventory = var.inventory - item.quantity
                var.inventory = inventory
                var.save()
                print("*****inventory", inventory)
                # item.save()

            if did_charge:
                order_obj.mark_paid() # sort a signal going to order's model mark_paid
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                order = str(order_obj)
                request.session['order_val'] = order
                return redirect('cart:sucess')
            if did_charge == False and ready:
                order_obj.mark_paid() # sort a signal going to order's model mark_paid
                request.session['cart_items'] = 0
                del request.session['cart_id']
                order = str(order_obj)
                request.session['order_val'] = order
                return redirect('cart:sucess')
            else:
                request.session['order'] = order_obj.order_id
                return redirect('cart:sucess')

    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "payment_choices": payment_choices,
        "payment_method": payment_method,
        "message": message,
        "error": error,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        # "shipping_address_required": shipping_address_required,
    }
    return render(request, "carts/checkout.html", context)

def create_payment_method(request):
    print("create_payment_method")
    context = {}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    cart_obj, cart_created = Cart.objects.new_or_get(request)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    context = {"object": order_obj}
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', None)
        order_obj.payment_method = payment_method
        order_obj.save()
        return redirect(next_)
    return render(request, 'carts/snippets/create_payment.html', context)



def choose_payment_method(request):
    print("choose_payment_method")
    context = {}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', None)
        print("payment_method***************", payment_method)
        if payment_method is not None:
            cart_obj, cart_created = Cart.objects.new_or_get(request)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
            order_obj.payment_method = payment_method
            order_obj.save()
    return redirect("cart:checkout")


def payment_cash(request):
    context = {}

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        amount = request.POST.get('amount', None)

        if amount is not None and amount != '':
            amount = Decimal(amount)
            cart_obj, cart_created = Cart.objects.new_or_get(request)
            billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
            order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
            order_obj.cash_amount = amount
            order_obj.save()
            # order_obj.cash_process()
    return redirect("cart:checkout")


def checkout_done_view(request, *args, **kwargs):

    user = True
    if request.user == "None":
        user = False

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    order_id = request.session.get('order_val')
    qs = Order.objects.get(order_id=order_id)

    context = {
        "user": user,
        "object": qs,
        "order_id": order_id
    }
    return render(request, "carts/checkout-done.html", context)
