from django.db import models
from django.utils.translation import gettext as _


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created timestamp'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Last updated at'))

    class Meta:
        abstract = True



