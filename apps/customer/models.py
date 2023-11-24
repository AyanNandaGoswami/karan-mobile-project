from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin
from .choices import TITLE_CHOICES
from apps.master.models import Village

User = get_user_model()


class Customer(TimeStampMixin):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT, help_text=_('Who added this customer?'), blank=True, null=True)
    # title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, null=True, verbose_name=_('Title'))
    first_name = models.CharField(max_length=50, verbose_name=_('First name of the customer'))
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Middle name of the customer'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last name of the customer'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email address of the customer'))
    mobile = models.CharField(max_length=12, verbose_name=_('Mobile number of the customer'))
    unique_id = models.CharField(max_length=25, blank=True, null=True, verbose_name=_('Customer unique ID'))

    # address
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Select village'))
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
        super(Customer, self).save()

    @property
    def name(self):
        return "%s%s%s" % (self.first_name, f' {self.middle_name} ' if self.middle_name else ' ', self.last_name)

    @property
    def customer_address(self):
        return "%s, %s, %s, %s, %s" % (self.village.name, self.post_office, self.district, self.state, self.pin_no)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

