# django
from django.dispatch import receiver
from django.db.models.signals import post_save

# local import
from .models import Invoices


@receiver(post_save, sender=Invoices)
def handle_invoice_post_save_signal(sender, instance, created, **kwargs):
    if created:
        instance.product.stock_quantity = instance.product.stock_quantity - instance.qty
        instance.product.save()

