# django
from django.contrib import admin

# local import
from .models import *


@admin.register(CustomerUniqueIdConfig)
class CustomerUniqueIdConfigAdmin(admin.ModelAdmin):
    list_display = ('preview', 'status')


@admin.register(ShopInformation)
class ShopInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(InvoicePDFTemplate)
