from django.contrib import admin

# Register your models here.

from .models import (
                Product,
                Variation,
                ProductFile,
                # CatalogCategory,
                # Catalog
                    )




class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0
    exclude = ['description']
    max_num = 10
    fields = ('title', 'price', 'sale_price', 'inventory', 'active', 'featured', 'presentation', 'min_qty')


class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image']
    inlines = [
            VariationInline, ProductFileInline,
    ]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

