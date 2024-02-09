from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import notify
from .models import Task
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(post_save, sender=Task)
def task_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.worker
        notification_text = instance.title
        notify.send(
            instance.created_by,
            recipient=recipient,
            verb="created",
            description=notification_text,
            target=instance,
        )

        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            notify.send(
                instance.created_by,
                recipient=superuser,
                verb="created",
                description=notification_text,
                target=instance,
            )
    else:
        recipient = instance.worker
        notification_text = instance.title
        notify.send(
            instance.created_by,
            recipient=recipient,
            verb="updated",
            description=notification_text,
            target=instance,
        )

        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            notify.send(
                instance.created_by,
                recipient=superuser,
                verb="updated",
                description=notification_text,
                target=instance,
            )


@receiver(post_delete, sender=Task)
def task_deleted_notification(sender, instance, **kwargs):
    if instance:
        recipient = instance.worker
        notification_text = instance.title
        notify.send(
            instance.created_by,
            recipient=recipient,
            verb="deleted",
            description=f'Task "{notification_text}" has been deleted.',
        )

        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            notify.send(
                instance.created_by,
                recipient=superuser,
                verb="deleted",
                description=f'Task "{notification_text}" has been deleted.',
            )
