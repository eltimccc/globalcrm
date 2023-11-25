# Generated by Django 4.2.7 on 2023-11-22 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("uploads", "0001_initial"),
        ("tasks", "0008_task_uploaded_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="uploaded_file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="task_files",
                to="uploads.uploadedfile",
            ),
        ),
    ]
