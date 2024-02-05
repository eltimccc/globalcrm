from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from .models import Task

@receiver(post_save, sender=Task)
def task_created_notification(sender, instance, created, **kwargs):
    if created:

        recipient = instance.worker
        notification_text = instance.title
        notify.send(instance.created_by, recipient=recipient, verb='created', description=notification_text, target=instance)
