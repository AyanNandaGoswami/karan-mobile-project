# django
from django.contrib import admin

# local import
from .models import *


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'unique_id')
    search_fields = ('first_name', 'middle_name', 'last_name', 'email', 'mobile', 'unique_id')
    search_help_text = 'Search by customer name, email, mobile, unique_id'
    raw_id_fields = ('added_by', )
    readonly_fields = ('post_office', 'district', 'state', 'pin_no', 'unique_id', 'added_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        obj.save()


