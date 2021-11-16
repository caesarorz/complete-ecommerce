import random
import os

# from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from rest_framework.reverse import reverse as api_reverse 

# from ecommerce.aws.utils import ProtectedS3Storage
from ecommerce.utils import unique_slug_generator, get_filename
from django.utils.safestring import mark_safe

from catalog.models import Catalog, CatalogCategory
# from catalog.models import CatalogCategory as categories

DEFAULT_CATALOG_ID = 1


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3966666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   # Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query) |
                   Q(title__startswith=query)
                   )

        return self.filter(lookups).distinct()

# it overwrites the object model manager in views.py


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_name(self):
        return self.title

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

    def get_related(self, instance):
        products_one = self.get_queryset().filter(category__in=instance.category.all())
        # products_two = self.get_queryset().filter(default=instance.default)
        qs = products_one.exclude(id=instance.id)
        return qs


class Product(models.Model):
    category = models.ManyToManyField(
        CatalogCategory, default=DEFAULT_CATALOG_ID, help_text="Categorias productos")
    # category        = models.ForeignKey('CatalogCategory', default=DEFAULT_COUNTRY_ID, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(
        max_length=120, help_text="Digite el nombre del producto")
    en_title = models.CharField(
        default="", max_length=120, help_text="Digite el nombre del producto")
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    en_description = models.TextField(default="")
    presentation = models.CharField(
        max_length=120, default="Peso", help_text="En que presentación se vende el producto")
    price = models.DecimalField(decimal_places=0, max_digits=10, null=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False)  # User Library
    default = models.ForeignKey(
        CatalogCategory, related_name="default_category", null=True, blank=True, on_delete=models.CASCADE)

    objects = ProductManager()

    # def get_absolute_url(self):
    #     # return "/products/{slug}/".format(slug=self.slug)
    #     return reverse("products:detail", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        # return "/products/{pk}/".format(pk=self.pk)
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    def get_api_url(self, request=None):
        return api_reverse("api-products:product-rud", kwargs={'pk': self.pk}, request=request)

    def get_image_url(self):
        img = self.image
        if img:
            return img.url
        return img  # return None

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{}/".format(slug)
    return location + filename  # "path/to/filename.mp4"


class ProductFile(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    file        = models.FileField(upload_to=upload_product_file_loc,
                                    storage=FileSystemStorage(location=settings.PROTECTED_ROOT))

    def __str__(self):
        return str(self.file.name)

    def get_download_url(self):
        return self.file.url
    
    @property
    def name(self):
        return self.file.name


class VariationQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    # def search(self, query):
    #     lookups = (Q(title__icontains=query) |
    #               # Q(description__icontains=query) |
    #               Q(price__icontains=query) |
    #               Q(tag__title__icontains=query) |
    #               Q(title__startswith=query)
    #               )

        # return self.filter(lookups).distinct()


class VariationManager(models.Manager):
    def get_queryset(self):
        return VariationQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None
    #
    # def search(self, query):
    #     return self.get_queryset().active().search(query)

    # def get_related(self, instance):
    #     variation_one = self.get_queryset().filter(category__in=instance.category.all())
    #     # products_two = self.get_queryset().filter(default=instance.default)
    #     qs = variation_one.exclude(id=instance.id)
    #     return qs


PRESENTATION = (
    ('unidad', 'la unidad'),
    ('peso', 'Kilo'),
)
STEP = (
    ('peso', '0.2'),
    ('unidad', '1')
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    en_title = models.CharField(default="", max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=0, max_digits=11)
    sale_price = models.DecimalField(
        decimal_places=0, max_digits=11, null=True, blank=True)
    active = models.BooleanField(default=True)
    step = models.DecimalField(
        default=0, choices=STEP, decimal_places=2, max_digits=6)
    presentation = models.CharField(
        max_length=120, choices=PRESENTATION, default='unidad')
    en_presentation = models.CharField(
        max_length=120, choices=PRESENTATION, default='unidad')
    # refer none == unlimited amount
    min_qty = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    featured = models.BooleanField(default=False)
    # refer none == unlimited amount
    inventory = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.title

    def get_presentation(self):
        if self.presentation == "peso":
            return "el kilo"
        return "la unidad"

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        print("get_price in products")
        if self.sale_price is not None:
            html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" % (
                self.sale_price, self.price)
        else:
            html_text = "<span class='price'>%s</span>" % (self.price)
        return mark_safe(html_text)

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.product.slug})

    def get_title(self):
        if self.product.title == self.title:
            return "{}".format(self.product.title)
            return "{} - {}".format(self.product.title, self.title)

    # def add_to_cart(self):
    #     return "{}?item={}&qty=1".format(reverse("cart-cbv"), self.id)
    #
    # def remove_from_cart(self):
    #     print("delete from models")
    #     return "{}?item={}&qty=1&delete=True".format(reverse("cart-cbv"), self.id)


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    print("* product", product)
    # reverse variation, no need to pull in the product variation
    variations = product.variation_set.all()
    # variation = Variation.objects.filter(product=product) like this one
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = product.title
        new_var.price = product.price
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)
