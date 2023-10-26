# django
from django.db.models.signals import post_save
from django.dispatch import receiver

# local import
from apps.settings.models import UniqueIdConfig
from .models import Customer


@receiver(post_save, sender=Customer)
def handle_customer_post_save_signal(sender, instance, created, **kwargs):
    if created and instance.unique_id is None:
        config = UniqueIdConfig.get_active_config(t='customer')
        if config:
            counter = config.counter or config.start_id
            counter += 1
            instance.unique_id = config.get_unique_id(counter=counter)

            # update counter
            config.counter = counter
            config.save()
        instance.save()

