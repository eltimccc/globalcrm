from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone

from clients.models import Client
from cars.models import Car
from prices.models import Tariff


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    rental_days = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_date} {self.client} {self.car}"
    
    # @property
    # def end_date(self):
    #     return self.start_date + timezone.timedelta(days=self.rental_days-1)

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timezone.timedelta(days=self.rental_days-1)
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Contract)
def set_tariff(sender, instance, **kwargs):
    if instance.car:
        instance.tariff = instance.car.tariff