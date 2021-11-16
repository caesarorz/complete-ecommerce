from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)



admin.site.register(Contact, ContactAdmin)
