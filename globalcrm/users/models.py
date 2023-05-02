from django.db import models


class Worker(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronomic = models.CharField(max_length=255)
    birth_date = models.DateField()
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"