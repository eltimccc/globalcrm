import os
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

from .filters import TaskFilter

from .models import Task, TaskExecution, TaskExecutionFile
from .forms import TaskExecutionForm, TaskForm, UpdateTaskExecutionForm, UpdateTaskForm
from django.utils.decorators import method_decorator
from notifications.models import Notification


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskListViewBase(ListView):
    model = Task
    context_object_name = "tasks"
    ordering = "created_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")

        filter = TaskFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(worker__username__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "created_at")
        return context


class TaskIndexView(TaskListViewBase):
    template_name = "tasks/index.html"


class AllTasksView(TaskListViewBase):
    template_name = "tasks/all_tasks.html"


class TasksFromMeView(TaskListViewBase):
    template_name = "tasks/from_me_tasks.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class TasksForMeView(TaskListViewBase):
    template_name = "tasks/for_me_tasks.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(worker=self.request.user)


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskExecutionForm()
        return context

    def get(self, request, *args, **kwargs):
        task = self.get_object()

        Notification.objects.filter(
            target_object_id=task.id, recipient=request.user, unread=True
        ).mark_all_as_read()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = not task.completed
        task.save()

        return redirect("tasks:task_detail", pk=task.pk)


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        file = self.request.FILES.get("file")
        if file:
            form.instance.file = file
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = "tasks/task_create.html"

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, "Вы не можете изменить эту задачу.")
        return super().handle_no_permission()

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks:index")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.created_by or self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseForbidden("403 Forbidden")

    def form_valid(self, form):
        task = self.get_object()
        Notification.objects.filter(target_object_id=task.id).delete()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks:index")

    
class TaskModalView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        executions = TaskExecution.objects.filter(task=task)
        execution_files = TaskExecutionFile.objects.filter(task_execution__in=executions)
        task_files = task.files.all()  

        task_files_names = [os.path.basename(file.file.name) for file in task_files]
        execution_files_names = [os.path.basename(file.file.name) for file in execution_files]
        
        data = {
            'task': task,
            'executions': executions,
            'task_files_names': task_files_names,
            'execution_files_names': execution_files_names,
        }
        html_modal_content = render_to_string('tasks/modal/task_modal.html', data)
        return JsonResponse({'html_modal_content': html_modal_content})


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskExecutionCreateView(LoginRequiredMixin, CreateView):
    model = TaskExecution
    form_class = TaskExecutionForm
    template_name = "tasks/task_detail.html"

    def get_task(self):
        return get_object_or_404(Task, pk=self.kwargs["task_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_task()
        context["xfiles"] = context["task"].files.all()
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

        for each in self.request.FILES.getlist("xfiles"):
            TaskExecutionFile.objects.create(task_execution=self.object, file=each)

        return response

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.get_task().pk})


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskExecutionDetailView(DetailView):
    model = TaskExecution
    template_name = "tasks/task_execution_detail.html"
    context_object_name = "task_execution"


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskExecutionUpdateView(UpdateView):
    model = TaskExecution
    form_class = UpdateTaskExecutionForm
    template_name = "tasks/task_create.html"

    def form_valid(self, form):
        task_execution = form.instance
        task = task_execution.task

        task.deadline = task_execution.deadline
        task.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskExecutionDeleteView(DeleteView):
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


def view_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user)

    return render(
        request,
        "notifications/view_notifications.html",
        {"notifications": notifications},
    )


class CompletedTaskListView(ListView):
    template_name = "tasks/completed_task_list.html"
    context_object_name = "completed_tasks"

    def get_queryset(self):
        return Task.objects.filter(worker=self.request.user, completed=True)

class TestTaskListView(TaskListViewBase):
    template_name = "tasks/test_page.html"
    
    