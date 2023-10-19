# django
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import Context, Template

# third party
import pdfkit

# local import
from django.conf import settings
from apps.settings.models import InvoicePDFTemplate, ShopInformation


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
    ctx = {
        'shop_name': shop_info.name,
        'subtitle': shop_info.subtitle,
        'shop_address': shop_info.address,
        'shop_logo_url': request.build_absolute_uri(shop_info.logo_for_invoice.url),
        'contact_no': shop_info.mobile,
        'alternative_contact_no': shop_info.alternative_contact,
        'bill_no': invoice.bill_no,
        'customer_name': invoice.customer.name,
        'customer_address': invoice.customer.customer_address,
        'customer_contact': invoice.customer.mobile,
        'purchase_date': invoice.purchase_date
    }
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
    response['Content-Disposition'] = 'attachment;' + f'filename={invoice.customer.name}_{invoice.product.name}.pdf'

    return response


generate_invoice_pdf.short_description = 'Download pdf for selected invoice'
