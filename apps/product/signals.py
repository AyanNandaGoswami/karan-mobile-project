# django
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction, models

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
        # map product price if cost is not defined in the form
        cost = instance.product.unit_price * instance.quantity
        instance.cost = cost
        instance.save()

    # update the total_invoice_price
    invoice = instance.invoice
    total_amt = invoice.invoice_items.aggregate(total_amt=models.Sum("cost"))['total_amt']
    total_amount = total_amt
    if invoice.discount:
        discount = round(total_amount * (invoice.discount / 100), 2)
        total_amount = total_amount - discount
    invoice.invoice_total = total_amount
    invoice.save()

