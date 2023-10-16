# django
from django.contrib import admin

# local import
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'unique_id')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'mobile')
    search_help_text = 'Search by customer name, email, mobile'
    raw_id_fields = ('added_by', 'village')
    readonly_fields = ('post_office', 'district', 'state', 'pin_no', 'unique_id')


