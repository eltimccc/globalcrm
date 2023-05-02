from django.db import models

from clients.models import Client
from cars.models import Car
from prices.models import Tariff


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rental_days = models.IntegerField()
    amount = models.DecimalField(max_digits=6,
                                 decimal_places=2,
                                 blank=True, null=True)

    def __str__(self):
        return f"{self.start_date} {self.client} {self.car}"

    def save(self, *args, **kwargs):
        self.rental_days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)

    