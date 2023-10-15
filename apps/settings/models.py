from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin


User = get_user_model()


class Village(TimeStampMixin):
    name = models.CharField(max_length=100, verbose_name=_('Name of the village'))
    post_office = models.CharField(verbose_name=_('Post Office name'))
    pin = models.IntegerField()


