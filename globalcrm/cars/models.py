from django.db import models

from prices.models import Tariff


class Car(models.Model):
    model = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=10)
    year = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=20)
    registration_date = models.DateField()
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.model} ({self.license_plate})"
