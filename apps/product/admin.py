from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path

# local import
from .models import *
from .admin_actions import generate_invoice_pdf
from .admin_forms import InvoiceItemAdminForm


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItems
    extra = 0
    verbose_name_plural = 'Invoice Items'
    verbose_name = 'Item'
    form = InvoiceItemAdminForm
    readonly_fields = ('taxable_amount', 'rate')


class InvoiceShipDetailInline(admin.TabularInline):
    model = InvoiceShipToDetail
    extra = 0
    verbose_name = 'Shipping Detail'
    verbose_name_plural = 'Shipping Details'
    readonly_fields = ('post_office', 'district', 'state', 'pin_no')


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ('invoice_no', 'sale_date', 'imei_no')
    raw_id_fields = ('created_by', 'customer', 'finance')
    readonly_fields = ('invoice_no', 'created_by')
    inlines = [InvoiceItemInline, InvoiceShipDetailInline]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

    def __init__(self, model, admin_site):
        self.list_display = ['invoice_no', 'customer_name', 'sale_date', 'invoice_pdf_button']
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
# admin.site.register(InvoiceItems)
# admin.site.register(InvoiceShipToDetail)

