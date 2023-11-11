from django import forms
from .models import Task, TaskExecution


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('worker', 'title', 'description', 'deadline', 'completed')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    success_url = '/'


class UpdateTaskForm(TaskForm):
    class Meta:
        model = Task
        fields = ['worker', 'title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }


class TaskExecutionForm(forms.ModelForm):
    class Meta:
        model = TaskExecution
        fields = ['task', 'title', 'description', 'deadline', 'created_at']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].widget = forms.HiddenInput()

class UpdateTaskExecutionForm(TaskForm):
    class Meta:
        model = TaskExecution
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }