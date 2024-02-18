from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future_date(value):
    if value < timezone.now():
        raise ValidationError('Дата дедлайна не может быть установлена на прошедшую дату.')

    