# Generated by Django 4.2 on 2023-11-11 20:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0006_remove_taskexecution_created_at_taskexecution_title_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="taskexecution",
            name="completed",
        ),
        migrations.AddField(
            model_name="taskexecution",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
