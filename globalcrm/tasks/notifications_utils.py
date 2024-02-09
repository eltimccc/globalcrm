# Это попробовать позже
from django.contrib.auth.models import User
from notifications.signals import notify


def send_notification(sender, recipient, verb, target, description):
    notify.send(
        sender, recipient=recipient, verb=verb, target=target, description=description
    )


def send_notification_for_object_created(sender, created_by, target, description):
    recipients = User.objects.filter(is_superuser=True)
    send_notification(sender, recipients, "created", target, description)


def send_notification_for_object_updated(sender, updated_by, target, description):
    recipients = User.objects.filter(is_superuser=True)
    send_notification(sender, recipients, "updated", target, description)


def send_notification_for_object_deleted(sender, deleted_by, target, description):
    recipients = User.objects.filter(is_superuser=True)
    send_notification(sender, recipients, "deleted", target, description)
