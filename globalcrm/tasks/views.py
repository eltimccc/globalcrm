import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from uploads.forms import FileUploadForm

from uploads.models import UploadedFile
from .models import Task, TaskExecution
from .forms import TaskExecutionForm, TaskForm, UpdateTaskExecutionForm, UpdateTaskForm
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.forms import inlineformset_factory


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class IndexView(TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sort_by = self.request.GET.get(
            "sort_by", "created_at"
        )  # По умолчанию сортировка по дате создания

        if sort_by == "completed":
            context["tasks"] = Task.objects.all().order_by("-completed", "created_at")
        elif sort_by == "created_at":
            context["tasks"] = Task.objects.all().order_by("created_at")
        elif sort_by == "worker":
            context["tasks"] = Task.objects.all().order_by("worker")
        elif sort_by == "created_by":
            context["tasks"] = Task.objects.all().order_by("created_by")
        elif sort_by == "deadline":
            context["tasks"] = Task.objects.all().order_by("deadline")

        return context


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_execution_form'] = TaskExecutionForm()
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        return redirect("tasks:task_detail", pk=task.pk)


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
# class CreateTaskView(LoginRequiredMixin, CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = "tasks/task_form.html"

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse("tasks:index")

class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:index")

@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class UpdateTaskView(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = "tasks/task_form.html"

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DeleteTaskView(DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:index")


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class FromMeTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/from_me_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    # Сортировка задач в профиле
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get(
            "sort_by", "created_at"
        )  # По умолчанию сортировка по дате создания

        if sort_by == "completed":
            context["tasks"] = context["tasks"].order_by("-completed", "created_at")
        elif sort_by == "created_at":
            context["tasks"] = context["tasks"].order_by("created_at")
        elif sort_by == "worker":
            context["tasks"] = context["tasks"].order_by("worker")
        elif sort_by == "created_by":
            context["tasks"] = context["tasks"].order_by("created_by")
        elif sort_by == "deadline":
            context["tasks"] = context["tasks"].order_by("deadline")

        return context


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class ForMeTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/for_me_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(worker=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get(
            "sort_by", "created_at"
        )  # По умолчанию сортировка по дате создания

        if sort_by == "completed":
            context["tasks"] = context["tasks"].order_by("-completed", "created_at")
        elif sort_by == "created_at":
            context["tasks"] = context["tasks"].order_by("created_at")
        elif sort_by == "worker":
            context["tasks"] = context["tasks"].order_by("worker")
        elif sort_by == "created_by":
            context["tasks"] = context["tasks"].order_by("created_by")
        elif sort_by == "deadline":
            context["tasks"] = context["tasks"].order_by("deadline")

        return context


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskExecutionCreateView(LoginRequiredMixin, CreateView):
    model = TaskExecution
    form_class = TaskExecutionForm
    template_name = "tasks/task_ex_create.html"

    def get_task(self):
        return get_object_or_404(Task, pk=self.kwargs["task_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_task()
        if context["task"].deadline:
            context["form"].fields["deadline"].initial = context[
                "task"
            ].deadline.strftime("%Y-%m-%dT%H:%M")
        return context

    def form_valid(self, form):
        form.instance.task = self.get_task()
        response = super().form_valid(form)
        task = self.get_task()
        task.deadline = form.instance.deadline
        task.save()
        return response

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.get_task().pk})


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskExecutionDetailView(DetailView):
    model = TaskExecution
    template_name = "tasks/task_execution_detail.html"
    context_object_name = "task_execution"


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class UpdateTaskExecution(UpdateView):
    model = TaskExecution
    form_class = UpdateTaskExecutionForm
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        task_execution = form.instance
        task = task_execution.task

        task.deadline = task_execution.deadline
        task.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class DeleteTaskExecutionView(DeleteView):
    model = TaskExecution
    template_name = "tasks/delete_task_execution.html"

    def get_object(self, queryset=None):
        task_execution = super().get_object(queryset)

        all_executions = TaskExecution.objects.filter(task=task_execution.task)
        previous_execution = (
            all_executions.exclude(pk=task_execution.pk).order_by("-created_at").first()
        )

        if previous_execution:
            task_execution.task.deadline = previous_execution.deadline
            task_execution.task.save()

        return task_execution

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_execution"] = self.get_object()
        return context

    def get_success_url(self):
        task_execution = self.get_object()
        return reverse_lazy("tasks:task_detail", kwargs={"pk": task_execution.task.pk})
