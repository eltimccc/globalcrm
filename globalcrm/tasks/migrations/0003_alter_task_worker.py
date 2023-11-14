# Generated by Django 4.2 on 2023-05-19 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0002_alter_task_worker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="worker",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="worker",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
