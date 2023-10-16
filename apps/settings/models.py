from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

# local import
from core.model_mixins import TimeStampMixin
from core.choices import STATUS_CHOICES

User = get_user_model()


class CustomerUniqueIdConfig(TimeStampMixin):
    prefix = models.CharField(max_length=5, blank=True, null=True)
    id_length = models.IntegerField()
    postfix = models.CharField(max_length=5, blank=True, null=True)
    start_id = models.IntegerField(default=0)
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
    def get_active_config():
        return CustomerUniqueIdConfig.objects.filter(status=1).last()

    class Meta:
        verbose_name = 'Unique ID configuration'
        verbose_name_plural = 'Customer unique-id configurations'

