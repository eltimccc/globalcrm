# Generated by Django 4.2 on 2023-05-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_profile_birth_date_alter_profile_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
