from django.db import models
from django.contrib.auth import get_user_model

# local import
from core.model_mixins import TimeStampMixin
from .choices import TITLE_CHOICES


User = get_user_model()


class Customers(TimeStampMixin):
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=12)
    formatted_id = models.CharField(max_length=25, blank=True, null=True)

    # address
    village = models.CharField(max_length=55)
    post_office = models.CharField(max_length=50)
    dist = models.CharField(max_length=)

