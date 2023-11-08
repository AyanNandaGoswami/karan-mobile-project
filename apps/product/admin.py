from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path

# local import
from .models import *
from .admin_actions import generate_invoice_pdf, preview_invoice
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
        self.list_display = ['invoice_no', 'customer_name', 'sale_date', 'invoice_view_button', 'invoice_pdf_button']
        super(InvoiceAdmin, self).__init__(model, admin_site)

    def invoice_view_button(self, obj):
        return format_html('<a href="{}" target="_blank" style="display: inline-block; padding: 6px 12px; background-color: #0074cc; color: #fff; text-decoration: none; border: 1px solid #0074cc; border-radius: 5px; text-align: center;">View</a>',
                           reverse('admin:preview-invoice') + '?ids={}'.format(obj.id))

    def invoice_pdf_button(self, obj):
        return format_html('<a href="{}" style="display: inline-block; padding: 6px 12px; background-color: #36a518; color: #fff; text-decoration: none; border: 1px solid #36a518; border-radius: 5px; text-align: center;">Download</a>',
                           reverse('admin:download-invoice-pdf') + '?ids={}'.format(obj.id))

    invoice_pdf_button.short_description = 'Download Invoice'
    invoice_view_button.short_description = 'View Invoice'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('download-invoice-pdf/', self.admin_site.admin_view(self.download_invoice_pdf_view), name='download-invoice-pdf'),
            path('preview-invoice', self.admin_site.admin_view(self.invoice_preview_view), name='preview-invoice'),
        ]
        return my_urls + urls

    def invoice_preview_view(self, request):
        ids = request.GET.getlist('ids')
        queryset = self.get_queryset(request).filter(id__in=ids)
        return preview_invoice(self, request, queryset)

    def download_invoice_pdf_view(self, request):
        ids = request.GET.getlist('ids')
        queryset = self.get_queryset(request).filter(id__in=ids)
        return generate_invoice_pdf(self, request, queryset)


admin.site.register(Invoices, InvoiceAdmin)

admin.site.register(Product)
admin.site.register(ProductType)
# admin.site.register(InvoiceItems)
# admin.site.register(InvoiceShipToDetail)

