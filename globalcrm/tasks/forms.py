from django import forms

from .models import Task, TaskExecution, TaskFile
from multiupload.fields import MultiFileField


class TaskForm(forms.ModelForm):
    uploaded_file = MultiFileField(required=False)

    class Meta:
        model = Task
        fields = [
            "worker",
            "title",
            "description",
            "deadline",
            "completed",
            "uploaded_file",
        ]

        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        if commit:
            task.save()

        for uploaded_file in self.cleaned_data.get("uploaded_file", []):
            TaskFile.objects.create(task=task, file=uploaded_file)

        return task


class UpdateTaskForm(TaskForm):
    class Meta:
        model = Task
        fields = ["worker", "title", "description", "deadline"]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class TaskExecutionForm(forms.ModelForm):
    class Meta:
        model = TaskExecution
        fields = ["task", "title", "description", "deadline", "created_at"]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = forms.HiddenInput()


class UpdateTaskExecutionForm(TaskExecutionForm):
    pass
