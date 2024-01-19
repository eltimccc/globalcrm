from django.db import models


class Tariff(models.Model):
    tarif_name = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2, default=2000)
    price_2_3_days = models.DecimalField(max_digits=6, decimal_places=2, default=1500)
    price_4_7_days = models.DecimalField(max_digits=6, decimal_places=2, default=1000)
    price_8_14_days = models.DecimalField(max_digits=6, decimal_places=2, default=500)
    price_15_30_days = models.DecimalField(max_digits=6, decimal_places=2, default=300)
    deposit = models.DecimalField(max_digits=6, decimal_places=2, default=6000)

    def __str__(self):
        return f"{self.pk}. Название тарифа: {self.tarif_name}"
