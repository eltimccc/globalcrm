# Generated by Django 4.2.7 on 2024-01-25 20:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("prices", "0002_alter_tariff_deposit_alter_tariff_price_15_30_days_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tariff",
            name="deposit",
            field=models.IntegerField(default=6000),
        ),
        migrations.AlterField(
            model_name="tariff",
            name="price_15_30_days",
            field=models.IntegerField(default=300),
        ),
        migrations.AlterField(
            model_name="tariff",
            name="price_2_3_days",
            field=models.IntegerField(default=1500),
        ),
        migrations.AlterField(
            model_name="tariff",
            name="price_4_7_days",
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name="tariff",
            name="price_8_14_days",
            field=models.IntegerField(default=500),
        ),
        migrations.AlterField(
            model_name="tariff",
            name="price_per_day",
            field=models.IntegerField(default=2000),
        ),
    ]
