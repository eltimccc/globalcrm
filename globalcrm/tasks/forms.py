from django import forms

from .models import Task, TaskExecution, TaskFile
from multiupload.fields import MultiFileField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


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
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            *self.Meta.fields,
            Submit('submit', 'Создать', css_class='btn-primary')
        )

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
        fields = ["title", "task", "description", "deadline", "created_at"]
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
            ),
            "created_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    xfiles = MultiFileField(
        required=False, min_num=1, max_num=5, max_file_size=1024 * 1024 * 5
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = forms.HiddenInput()

        # Определение FormHelper для Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Добавить"))
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"


class UpdateTaskExecutionForm(TaskExecutionForm):
    pass
