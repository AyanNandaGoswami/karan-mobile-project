# django
from django.db.models.signals import post_save
from django.dispatch import receiver

# local import
from .models import CustomerUniqueIdConfig


# @receiver(post_save, sender=CustomerUniqueIdConfig)
# def handle_customer_id_config_post_save_signal(sender, instance, created, **kwargs):


