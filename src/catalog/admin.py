from django.contrib import admin

from django.contrib import admin

# Register your models here.

from .models import (
                CatalogCategory,
                Catalog
                    )


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'pub_date')

admin.site.register(Catalog, CatalogAdmin)

class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent')

admin.site.register(CatalogCategory, CatalogCategoryAdmin)
