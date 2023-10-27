# django
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction

# local import
from .models import Invoices, InvoiceItems
from apps.settings.models import UniqueIdConfig


@receiver(post_save, sender=Invoices)
def handle_invoice_post_save_signal(sender, instance, created, **kwargs):
    with transaction.atomic():
        if created:
            if instance.invoice_no is None:
                config = UniqueIdConfig.get_active_config(t='invoice')
                if config:
                    counter = config.counter or config.start_id
                    counter += 1
                    instance.invoice_no = config.get_unique_id(counter=counter)

                    # update counter
                    config.counter = counter
                    config.save()  # update config counter
            instance.save()  # update invoice


@receiver(post_save, sender=InvoiceItems)
def handle_invoiceitem_post_save_signal(sender, instance, created, **kwargs):
    if created:
        instance.product.stock_quantity = instance.product.stock_quantity - instance.quantity
        instance.product.save()  # update product

    if not instance.cost:
        cost = instance.product.unit_price * instance.quantity
        instance.cost = cost
        gst = 1.18  # 18%
        rate = round(cost / gst, 2)
        taxable_amount = round(cost - rate, 2)
        instance.taxable_amount = taxable_amount
        instance.rate = rate
        instance.save()

