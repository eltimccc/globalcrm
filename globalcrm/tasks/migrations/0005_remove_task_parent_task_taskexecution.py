# Generated by Django 4.2 on 2023-11-10 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_parent_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='parent_task',
        ),
        migrations.CreateModel(
            name='TaskExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='Описание выполнения задачи')),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='executions', to='tasks.task')),
            ],
        ),
    ]