from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin
from apps.customer.models import Customer
from apps.master.models import Finance, Village
from apps.settings.models import InvoiceConfiguration

User = get_user_model()


class ProductType(TimeStampMixin):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'


class Product(TimeStampMixin):
    name = models.CharField(max_length=255, verbose_name=_('Name of the Product'))
    code = models.CharField(max_length=15, verbose_name=_('Product code'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Product description'))
    unit_price = models.FloatField(verbose_name=_('Price'))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Stock quantity'))
    p_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product type'))

    def __str__(self):
        return self.name

    @property
    def available(self):
        mapped_dict = {True: 'Yes', False: 'No'}
        return mapped_dict.get(self.stock_quantity >= 1)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Invoices(TimeStampMixin):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Sold by'), blank=True, null=True)
    invoice_no = models.CharField(blank=True, null=True, verbose_name=_('Invoice No.'), max_length=25)
    sale_date = models.DateField(verbose_name=_("Date of sale"), blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'), help_text=_('Choose one customer'))
    discount = models.IntegerField(default=0, verbose_name=_('Discount(%)'))
    # invoice_total = models.FloatField(default=0, verbose_name=_('Invoice total'))
    paid_amount = models.IntegerField(default=0, verbose_name=_('Paid amount'))
    ship_to_as_bill_to = models.BooleanField(default=False, verbose_name=_('Ship to same as bill to'))
    customer_signature = models.BooleanField(default=False, verbose_name=_('Show Customer Signature box on invoice'))

    # finance
    finance = models.ForeignKey(Finance, on_delete=models.SET_NULL, blank=True, null=True)
    dp = models.FloatField(default=0, verbose_name=_('Down payment'))
    emi = models.FloatField(default=0, verbose_name=_('EMI per month'))
    total_month = models.IntegerField(default=0, verbose_name=_('Total months to pay EMI'))
    margin_money = models.IntegerField(default=0, verbose_name=_('Margin Money'))
    advance_emi = models.IntegerField(default=0, verbose_name=_('Advance EMI'))
    loan_number = models.CharField(max_length=15, blank=True, null=True)

    #
    trash = models.BooleanField(default=False)

    def __str__(self):
        return "%s | %s" % (self.invoice_no, self.customer.name)

    @property
    def customer_name(self):
        return self.customer.name

    @property
    def items(self):
        return InvoiceItems.objects.filter(invoice=self)

    @property
    def total_amount_and_qty(self):
        return InvoiceItems.objects.filter(invoice=self).aggregate(
            total_amt=models.Sum("cost"), total_qty=models.Sum("quantity"), total_tax=models.Sum("taxable_amount"))

    @property
    def invoice_total_amount(self):
        invoice_total = InvoiceItems.objects.filter(invoice=self).aggregate(total_amt=models.Sum("cost"))['total_amt']
        invoice_total = invoice_total or 0
        # apply discount if possible
        if self.discount:
            discount = round(invoice_total * (self.discount / 100), 2)
            invoice_total = invoice_total - discount
        return invoice_total

    @property
    def formatted_date(self):
        invoice_conf = InvoiceConfiguration.objects.last()

        format_conf = {
            'format_1': self.sale_date.strftime("%b %d, %Y"),
            'format_2': self.sale_date.strftime("%d/%m/%Y"),
            'format_3': self.sale_date.strftime("%m/%d/%Y"),
            'format_4': self.sale_date.strftime("%Y/%m/%d"),
            'format_5': self.sale_date.strftime("%d-%m-%Y"),
            'format_6': self.sale_date.strftime("%m-%d-%Y"),
            'format_7': self.sale_date.strftime("%Y-%m-%d"),
            'format_8': self.sale_date.strftime("%d %b, %Y"),
        }
        return format_conf.get(invoice_conf.date_format)

    @property
    def payment_balance(self):
        return 0 if self.finance else int(self.invoice_total_amount - float(self.paid_amount))

    @property
    def payment_method(self):
        return self.finance.name if self.finance else 'Cash'

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class InvoiceItems(TimeStampMixin):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE, verbose_name=_('Invoice'),
                                help_text=_('Select invoice'), related_name='invoice_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'),
                                help_text=_('Choose your desired product'))
    imei_no = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('IMEI No.'), help_text=_('Enter the unique IMEI No.'))
    serial_no = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Serial no.'), help_text=_('Enter the serial no.'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    cost = models.FloatField(default=0, verbose_name=_('Price'))
    rate = models.FloatField(default=0, verbose_name=_('Rate'))
    taxable_amount = models.FloatField(default=0, verbose_name=_('Taxable amount'))

    def __str__(self):
        return "Invoice: %s | Product: %s" % (self.invoice, self.product)

    @property
    def serial_or_imei(self):
        return self.imei_no or self.serial_no or ''

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.cost:
            # calculate GST based on cost
            gst = 1.18  # 18%
            rate = round(self.cost / gst, 2)
            taxable_amount = round(self.cost - rate, 2)
            self.taxable_amount = taxable_amount
            self.rate = rate
        super(InvoiceItems, self).save()

    class Meta:
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'


class InvoiceShipToDetail(TimeStampMixin):
    invoice = models.OneToOneField(Invoices, on_delete=models.CASCADE, verbose_name=_('Invoice'),
                                   help_text=_('Select invoice'), related_name='invoice_ship_detail')
    name = models.CharField(max_length=255, verbose_name=_("Name"), blank=True, null=True)
    mobile_no = models.CharField(max_length=10, verbose_name=_('Contact No.'), blank=True, null=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name=_('Select village'))
    post_office = models.CharField(max_length=75, blank=True, null=True, verbose_name=_('Post office'))
    district = models.CharField(max_length=75, blank=True, null=True, verbose_name=_('District'))
    state = models.CharField(max_length=55, blank=True, null=True, verbose_name=_('State'))
    pin_no = models.IntegerField(blank=True, null=True, verbose_name=_('PIN code number'))

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.village:
            self.post_office = self.village.post_office.name
            self.district = self.village.post_office.dist.name
            self.state = self.village.post_office.dist.state.name
            self.pin_no = self.village.post_office.pin_no
        super(InvoiceShipToDetail, self).save()

    @property
    def contact(self):
        return self.mobile_no or ''

    @property
    def address(self):
        return "%s, %s, %s, %s, %s" % (self.village.name, self.post_office, self.district, self.state, self.pin_no)

    class Meta:
        verbose_name = 'Ship to detail'
        verbose_name_plural = 'Invoice Ship To Details'
