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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Invoices(TimeStampMixin):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Sold by'))
    bill_no = models.IntegerField(blank=True, null=True, verbose_name=_('Bill No.'))
    purchase_date = models.DateField(verbose_name=_("Purchase date"))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'), help_text=_('Choose one customer'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'),
                                help_text=_('Choose your desired product'))
    imei_no = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('IMEI No.'), help_text=_('Enter the unique IMEI No.'))
    qty = models.IntegerField(default=0, verbose_name=_('Quantity'))
    finance = models.ForeignKey(Finance, on_delete=models.SET_NULL, blank=True, null=True)
    dp = models.FloatField(default=0, verbose_name=_('Down payment'))
    emi = models.FloatField(default=0, verbose_name=_('EMI per month'))
    total_month = models.IntegerField(default=0, verbose_name=_('Total months to pay EMI'))

    def __str__(self):
        return "%s | %s" % (self.bill_no, self.customer.name)

    @property
    def customer_name(self):
        return self.customer.name

    @property
    def product_name(self):
        return self.product.name

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

