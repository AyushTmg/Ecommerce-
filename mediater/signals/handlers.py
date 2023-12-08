from primary.signals import order_created
from django.dispatch import receiver

@receiver(order_created)
def on_created(sender, **kwargs):
    print(sender)
    print(kwargs['order'])
