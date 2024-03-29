# Generated by Django 4.2 on 2023-05-19 09:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_profile_delete_worker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="profile",
            name="patronomic",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="profile",
            name="position",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="profile",
            name="surname",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
