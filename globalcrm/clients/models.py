from datetime import datetime
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronomic = models.CharField(max_length=255)
    birth_date = models.DateTimeField(default=datetime(1990, 1, 1))
    passport_series_number = models.CharField(max_length=20)
    passport_issue_date = models.DateTimeField(default=datetime(1990, 1, 1))
    passport_issued_by = models.CharField(max_length=100)
    # country = models.CharField(max_length=100, verbose_name='Страна', default='Россия')
    # city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=100, verbose_name='Улица, дом, квартира')
    driving_number = models.CharField(max_length=20)
    driver_license_issue_date = models.DateTimeField(default=datetime(1990, 1, 1))
    driver_license_valid_until = models.DateTimeField(default=datetime(1990, 1, 1))
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
