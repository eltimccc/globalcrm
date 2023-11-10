from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Task(models.Model):
    worker = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="worker")
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, default=1, related_name='created_by')
    title = models.CharField(max_length=200, default='Название задачи')
    description = models.TextField(default='Описание задачи')
    deadline = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        timezone.activate('Europe/Moscow')
        super().save(*args, **kwargs)

class TaskExecution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='executions')
    description = models.TextField(default='Описание выполнения задачи')
    deadline = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'История выполнения для задачи "{self.task.title}"'

@receiver(pre_save, sender=Task)
def set_completed_at(sender, instance, **kwargs):
    if instance.completed and not instance.completed_at:
        instance.completed_at = timezone.now()
    elif not instance.completed:
        instance.completed_at = None
