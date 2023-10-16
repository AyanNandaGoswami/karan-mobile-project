from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin


User = get_user_model()


class State(TimeStampMixin):
    name = models.CharField(max_length=55, verbose_name=_('Name of the state'))
    code = models.CharField(blank=True, null=True, max_length=10, verbose_name=_('State code'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')


class District(TimeStampMixin):
    name = models.CharField(max_length=75, verbose_name=_('Name of the district'))
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_('Select state'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')


class PostOffice(TimeStampMixin):
    name = models.CharField(max_length=75, verbose_name=_('Name of the Post office'))
    pin_no = models.IntegerField(verbose_name=_('PIN code number'))
    dist = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('Select district'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Post Office')
        verbose_name_plural = _('Post offices')


class Village(TimeStampMixin):
    name = models.CharField(max_length=100, verbose_name=_('Name of the village'))
    post_office = models.ForeignKey(PostOffice, on_delete=models.CASCADE, verbose_name=_('Select post office'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Village')
        verbose_name_plural = _('Villages')


