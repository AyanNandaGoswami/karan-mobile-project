# django
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Context, Template

# third party
import pdfkit
from num2words import num2words

# local import
from django.conf import settings
from apps.settings.models import InvoicePDFTemplate, ShopInformation, InvoiceConfiguration
from .models import InvoiceShipToDetail


def generate_valid_strings(plain_text, context):
    '''
    This function is to bind the plain text with their respective variable..{{var}}
    Example:
        input: <p>Hey {{ user_account.first_name }}, welcome!</p>
        output: <p>Hey Brett, welcome!</p>
    '''
    template = Template(plain_text)
    context = Context(context)
    generated_string = template.render(context)
    return generated_string


def get_context(invoice, request) -> dict:
    shop_info = ShopInformation.objects.last()
    invoice_total_info = invoice.total_amount_and_qty
    invoice_conf, created = InvoiceConfiguration.objects.get_or_create()
    shipping_detail = InvoiceShipToDetail.objects.filter(invoice=invoice).last()
    ctx = {
        'shop_info': shop_info,
        'invoice': invoice,
        'shop_logo_url': request.build_absolute_uri(shop_info.logo_for_invoice.url),
        'digital_sig_url': request.build_absolute_uri(shop_info.digital_signature.url) if shop_info.digital_signature else '',
        'payment_qr_url': request.build_absolute_uri(shop_info.payment_qr.url) if shop_info.payment_qr else '',
        'invoice_total_amt': invoice_total_info['total_amt'],   # without discount calculation
        'invoice_total_quantity': invoice_total_info['total_qty'],
        'invoice_total_tax': round(invoice_total_info['total_tax'], 2) if invoice_total_info['total_tax'] else None,
        'invoice_conf': invoice_conf,
        'shipping_detail': shipping_detail,
        'taxable_amount': sum([i.rate for i in invoice.items])
    }
    ctx['tax'] = round(ctx['invoice_total_tax'] / 2, 2) if ctx['invoice_total_tax'] else None
    if invoice.discount:
        ctx['discount'] = round(ctx['invoice_total_amt'] * (invoice.discount / 100), 2)
        ctx['invoice_total'] = ctx['invoice_total_amt'] - ctx['discount']
    else:
        ctx['invoice_total'] = ctx['invoice_total_amt']
    if invoice_conf.round_off:
        ctx['round_off'] = round(ctx['invoice_total'] - int(ctx['invoice_total']), 2)
        ctx['invoice_total'] = int(ctx['invoice_total'])
    ctx['amt_in_words'] = num2words(ctx['invoice_total']).capitalize()
    return ctx


def generate_invoice_pdf(modeladmin, request, queryset):
    # Optional configuration options for pdfkit
    options = {
        'page-size': 'Letter',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm'
    }

    invoice = queryset.last()
    context = get_context(invoice, request)
    template_config = InvoicePDFTemplate.objects.last()
    html_content = generate_valid_strings(template_config.template, context)

    # Use pdfkit to convert the HTML content to PDF
    pdf_content = pdfkit.from_string(html_content, False, options=options)

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;' + f'filename={invoice.customer.name}_{invoice.invoice_no}.pdf'

    return response


generate_invoice_pdf.short_description = 'Download pdf for selected invoice'
