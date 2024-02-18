from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future_date(value):
    print("Валидатор вызван")
    if value < timezone.now():
        raise ValidationError('Дата выполнения не может быть установлена на прошедшую дату!')

    