from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    patronomic = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def formatted_birth_date(self):
        if self.birth_date:
            return self.birth_date.strftime("%d.%m.%Y")
        return ""

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"