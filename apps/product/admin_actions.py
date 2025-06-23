# django
from django.http import HttpResponse
from django.template import Context, Template

# third party
import pdfkit
from num2words import num2words
from playwright.sync_api import sync_playwright

# local import
from apps.settings.models import InvoicePDFTemplate, ShopInformation, InvoiceConfiguration
from .models import InvoiceShipToDetail
from mobile_shop_project.settings import USE_PLAYWRIGHT_FOR_PDF


def generate_valid_strings(plain_text, context):
    """
    This function is to bind the plain text with their respective variable..{{var}}
    Example:
        input: <p>Hey {{ user_account.first_name }}, welcome!</p>
        output: <p>Hey Brett, welcome!</p>
    """
    template = Template(plain_text)
    context = Context(context)
    generated_string = template.render(context)
    return generated_string


def get_finance_note(invoice):
    if invoice.finance:
        context = {
            'advance_emi': int(invoice.advance_emi),
            'margin_money': int(invoice.margin_money),
            'down_payment': int(invoice.dp),
            'per_month_emi': int(invoice.emi),
            'total_month': int(invoice.total_month)
        }
        return generate_valid_strings(invoice.finance.finance_note, context)
    return None


def get_context(invoice, request) -> dict:
    shop_info = invoice.store or ShopInformation.objects.last() or ShopInformation.objects.create()
    invoice_total_info = invoice.total_amount_and_qty
    invoice_conf = InvoiceConfiguration.objects.last() or InvoiceConfiguration.objects.create()
    shipping_detail = InvoiceShipToDetail.objects.filter(invoice=invoice).last()
    ctx = {
        'shop_info': shop_info,
        'invoice': invoice,
        'shop_logo_url': request.build_absolute_uri(shop_info.logo_for_invoice.url) if shop_info.logo_for_invoice else '',
        'digital_sig_url': request.build_absolute_uri(shop_info.digital_signature.url) if shop_info.digital_signature else '',
        'payment_qr_url': request.build_absolute_uri(shop_info.payment_qr.url) if shop_info.payment_qr else '',
        'invoice_total_amt': invoice_total_info['total_amt'],   # without discount calculation
        'invoice_total_quantity': invoice_total_info['total_qty'],
        'invoice_total_tax': round(invoice_total_info['total_tax'], 2) if invoice_total_info['total_tax'] else None,
        'invoice_conf': invoice_conf,
        'shipping_detail': shipping_detail,
        'taxable_amount': round(sum([i.rate for i in invoice.items]), 2),
        'finance_note': get_finance_note(invoice=invoice)
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
    ctx['amt_in_words'] = num2words(ctx['invoice_total']).capitalize() if ctx['invoice_total'] else None
    return ctx


# Legacy method using pdfkit + wkhtmltopdf
# Works on Linux/Mac but often has issues on Windows due to wkhtmltopdf path/config problems, and it does not support
# modern CSS on windows
def generate_invoice_pdf_using_pdfkit(modeladmin, request, queryset):
    # PDF rendering options
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

    try:
        # Convert HTML to PDF using pdfkit (requires wkhtmltopdf installed and on PATH)
        pdf_content = pdfkit.from_string(html_content, False, options=options)

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="{invoice.customer.name}_{invoice.invoice_no}.pdf"'
        )
        return response

    except OSError as e:
        # If wkhtmltopdf is not available or fails, return an error
        return HttpResponse(f"PDF generation failed: {str(e)}", status=500)


def generate_invoice_pdf_using_playwright(modeladmin, request, queryset):
    invoice = queryset.last()
    context = get_context(invoice, request)
    template_config = InvoicePDFTemplate.objects.last()
    html_content = generate_valid_strings(template_config.template, context)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Set page content to the generated HTML
        page.set_content(html_content, wait_until="networkidle")

        # Generate the PDF in memory (don't save to disk)
        pdf_content = page.pdf(
            format="Letter",
            scale=context['invoice_conf'].pdf_scale if context['invoice_conf'] else 0.7,
            print_background=True
        )

        browser.close()

    # Return the PDF as an HTTP response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="{invoice.customer.name}_{invoice.invoice_no}.pdf"'
    )

    return response


def preview_invoice(modeladmin, request, queryset):
    invoice = queryset.last()
    context = get_context(invoice, request)
    template_config = InvoicePDFTemplate.objects.last()
    html_content = generate_valid_strings(template_config.template, context)
    return HttpResponse(html_content)


def generate_invoice_pdf_response(modeladmin, request, queryset):
    """
    main selector function to generate invoice PDF
    chooses between Playwright and PDFKit depending on configuration
    """
    if USE_PLAYWRIGHT_FOR_PDF:
        return generate_invoice_pdf_using_playwright(modeladmin, request, queryset)
    else:
        return generate_invoice_pdf_using_pdfkit(modeladmin, request, queryset)


preview_invoice.short_description = 'View Invoice'
generate_invoice_pdf_response.short_description = 'Download pdf for selected invoice'
