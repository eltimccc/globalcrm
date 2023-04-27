from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    worker = models.TextField(default='eltimc')
    created_by = models.ForeignKey(User,
                                   on_delete=models.PROTECT,
                                   default=1)
    content = models.TextField(default='Регистрация')
    deadline = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content