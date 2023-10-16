# django
from django.contrib import admin

# local import
from .models import *


@admin.register(CustomerUniqueIdConfig)
class CustomerUniqueIdConfigAdmin(admin.ModelAdmin):
    list_display = ('preview', 'status')

