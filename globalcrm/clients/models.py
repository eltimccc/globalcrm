from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    patronomic = models.CharField(max_length=255)
    birth_date = models.DateField()
    passport_series_number = models.CharField(max_length=20)
    passport_issue_date = models.DateField()
    passport_issued_by = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    driving_number = models.CharField(max_length=20) 
    driver_license_issue_date = models.DateField()
    driver_license_valid_until = models.DateField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
