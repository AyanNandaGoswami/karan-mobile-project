from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin
from apps.customer.models import Customer
from apps.master.models import Finance

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
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Stock quantity'))
    p_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product type'))
    serial_no = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Invoices(TimeStampMixin):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Sold by'), blank=True, null=True)
    invoice_no = models.CharField(blank=True, null=True, verbose_name=_('Invoice No.'), max_length=25)
    sale_date = models.DateField(verbose_name=_("Date of sale"), blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'), help_text=_('Choose one customer'))
    finance = models.ForeignKey(Finance, on_delete=models.SET_NULL, blank=True, null=True)
    dp = models.FloatField(default=0, verbose_name=_('Down payment'))
    emi = models.FloatField(default=0, verbose_name=_('EMI per month'))
    total_month = models.IntegerField(default=0, verbose_name=_('Total months to pay EMI'))

    def __str__(self):
        return "%s | %s" % (self.invoice_no, self.customer.name)

    @property
    def customer_name(self):
        return self.customer.name

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'


class InvoiceItems(TimeStampMixin):
    invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE, verbose_name=_('Invoice'),
                                help_text=_('Select invoice'), related_name='invoice_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'),
                                help_text=_('Choose your desired product'))
    imei_no = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('IMEI No.'), help_text=_('Enter the unique IMEI No.'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))

    def __str__(self):
        return "Invoice: %s | Product: %s" % (self.invoice, self.product)

    class Meta:
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'

