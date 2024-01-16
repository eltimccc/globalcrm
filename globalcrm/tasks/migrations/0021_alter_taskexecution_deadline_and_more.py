# Generated by Django 4.2.7 on 2024-01-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0020_alter_taskexecution_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskexecution",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="taskexecution",
            name="description",
            field=models.TextField(default="Описание задачи"),
        ),
        migrations.AlterField(
            model_name="taskexecution",
            name="title",
            field=models.CharField(default="Название задачи", max_length=200),
        ),
    ]