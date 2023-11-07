from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# third party
from ckeditor.fields import RichTextField

# local import
from core.model_mixins import TimeStampMixin
from core.choices import STATUS_CHOICES
from .choices import UNIQUE_ID_CHOICE

User = get_user_model()


class UniqueIdConfig(TimeStampMixin):
    type = models.CharField(choices=UNIQUE_ID_CHOICE, default='customer', max_length=10)
    prefix = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('Prefix for Customer-Id'))
    id_length = models.IntegerField(verbose_name=_('Length of Customer-Id'))
    postfix = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('Postfix for Customer-Id'))
    start_id = models.IntegerField(default=0, verbose_name=_('Start indexing id'))
    counter = models.IntegerField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    def __str__(self):
        return self.preview

    @property
    def preview(self):
        return "%s%s%s" % (self.prefix if self.prefix else '', str(self.start_id).zfill(
            self.id_length - ((len(self.prefix) if self.prefix else 0) + (len(self.postfix) if self.postfix else 0))),
                           self.postfix if self.postfix else '')

    def get_unique_id(self, counter):
        return "%s%s%s" % (self.prefix if self.prefix else '', str(counter).zfill(
            self.id_length - ((len(self.prefix) if self.prefix else 0) + (len(self.postfix) if self.postfix else 0))),
                           self.postfix if self.postfix else '')

    @staticmethod
    def get_active_config(t: str):
        return UniqueIdConfig.objects.filter(status=1, type=t).last()

    class Meta:
        verbose_name = 'Unique-ID configuration'
        verbose_name_plural = 'Unique-ID configurations'


class ShopInformation(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name=_('Shop name'))
    subtitle = models.CharField(max_length=255, verbose_name=_('Subtitle of shop'), blank=True, null=True)
    owner_name = models.CharField(max_length=255, verbose_name=_('Shop owner name'))
    mobile = models.CharField(max_length=10, verbose_name=_('Contact no.'))
    alternative_contact = models.CharField(max_length=10, verbose_name=_('Alternative contact no.'), blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name=_('Shop email address'))
    website = models.URLField(blank=True, null=True, verbose_name=_('Shop website'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Shop Address'),
                               help_text=_('Enter the address you want to appear on invoices.'))
    logo_for_invoice = models.ImageField(upload_to='shop-info/invoice-logo/', blank=True, null=True)
    gst_no = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('GST No.'))
    digital_signature = models.ImageField(upload_to='shop-info/digital-signature/', blank=True, null=True)
    # bank details
    ac_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('A/C Name'))
    bank_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Bank Name'))
    ac_no = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('A/C No.'))
    ifsc = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('IFSC No.'))
    branch = models.CharField(max_length=35, blank=True, null=True, verbose_name=_('Branch'))
    payment_qr = models.ImageField(upload_to='shop-info/payment-qr/', blank=True, null=True, verbose_name=_('Payment QR'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shop Information'
        verbose_name_plural = 'Shop Information'


class InvoicePDFTemplate(TimeStampMixin):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    template = RichTextField(verbose_name=_('Template Preview'))

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _('Invoice Template')
        verbose_name_plural = _('Invoice PDF Templates')


class InvoiceConfiguration(TimeStampMixin):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    show_bank_detail = models.BooleanField(default=False, verbose_name=_('Show bank details on invoices'))
    show_tax_invoice = models.BooleanField(default=False, verbose_name=_('Show "Tax Invoice" on invoices'))
    show_quotation = models.BooleanField(default=False, verbose_name=_('Show "Quotation" on invoices'))
    digital_signature = models.BooleanField(default=False, verbose_name=_('Enable digital signatures on invoices'))
    show_finance_details = models.BooleanField(default=False, verbose_name=_('Show finance details on invoices'))
    show_qr_code = models.BooleanField(default=False, verbose_name=_('Show QR code on invoice'))
    round_off = models.BooleanField(default=False, verbose_name=_('Enable round-off'))
    original_for_recipient = models.BooleanField(default=False, verbose_name=_('Show "ORIGINAL FOR RECIPIENT"'))

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Invoice Configuration'
        verbose_name_plural = 'Invoice Configurations'

