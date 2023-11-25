# Generated by Django 4.2.7 on 2023-11-25 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0017_remove_task_uploaded_file_taskfile"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskExecutionFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                (
                    "task_execution",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="tasks.taskexecution",
                    ),
                ),
            ],
        ),
    ]
