from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path

# local import
from .models import *
from .admin_actions import generate_invoice_pdf


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ('bill_no', 'purchase_date', 'imei_no')
    raw_id_fields = ('created_by', 'product', 'customer', 'finance')

    def __init__(self, model, admin_site):
        self.list_display = ['id', 'customer_name', 'product_name', 'purchase_date', 'invoice_pdf_button']
        super(InvoiceAdmin, self).__init__(model, admin_site)

    def invoice_pdf_button(self, obj):
        return format_html('<a class="button" href="{}">Download Invoice</a>',
                           reverse('admin:download-invoice-pdf') + '?ids={}'.format(obj.id))

    invoice_pdf_button.short_description = 'Invoice'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('download-invoice-pdf/', self.admin_site.admin_view(self.download_invoice_pdf_view), name='download-invoice-pdf'),
        ]
        return my_urls + urls

    def download_invoice_pdf_view(self, request):
        ids = request.GET.getlist('ids')
        queryset = self.get_queryset(request).filter(id__in=ids)
        return generate_invoice_pdf(self, request, queryset)


admin.site.register(Invoices, InvoiceAdmin)

admin.site.register(Product)
admin.site.register(ProductType)


