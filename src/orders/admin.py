from django.contrib import admin

from .models import Order, ProductPurchase  #, UserCheckout

# Register your models here.


admin.site.register(Order)

admin.site.register(ProductPurchase)

# admin.site.register(UserCheckout)
