# django
from django.db.models.signals import post_save
from django.dispatch import receiver

# local import
from apps.settings.models import CustomerUniqueIdConfig
from .models import Customer


@receiver(post_save, sender=Customer)
def handle_customer_post_save_signal(sender, instance, created, **kwargs):
    if created and instance.unique_id is None:
        config = CustomerUniqueIdConfig.get_active_config()
        if config:
            print(config.counter)
            print(config.start_id)
            counter = config.counter or config.start_id + 1
            print(counter)
            instance.unique_id = config.get_unique_id(counter=counter)

            # update counter
            config.counter = counter
            config.save()
        instance.save()

