from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


class BaseTask(models.Model):
    title = models.CharField(max_length=200, default="Название задачи")
    description = models.TextField(default="Описание задачи")
    deadline = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Task(BaseTask):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, default=1, related_name="created_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    worker = models.ForeignKey(
        User, on_delete=models.PROTECT, default=None, related_name="worker"
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)


    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.pk})

    @property
    def files(self):
        return TaskFile.objects.filter(task=self)


class TaskExecution(BaseTask):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.task.title
        super().save(*args, **kwargs)

    @property
    def files(self):
        return TaskExecutionFile.objects.filter(task_execution=self)


class TaskFile(models.Model):
    task = models.ForeignKey("Task", related_name="file", on_delete=models.PROTECT)
    file = models.FileField(upload_to="uploads/")


class TaskExecutionFile(models.Model):
    task_execution = models.ForeignKey(
        "TaskExecution", related_name="xfiles", on_delete=models.PROTECT
    )
    file = models.FileField(upload_to="uploads/")


@receiver(pre_save, sender=Task)
def set_completed_at(sender, instance, **kwargs):
    if instance.completed and not instance.completed_at:
        instance.completed_at = timezone.now()
    elif not instance.completed:
        instance.completed_at = None
