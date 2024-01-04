from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from .models import Task, TaskExecution, TaskExecutionFile
from .forms import TaskExecutionForm, TaskForm, UpdateTaskExecutionForm, UpdateTaskForm
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class IndexView(View):
    template_name = "tasks/index.html"

    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get("sort_by", "created_at")
        ordering = self.get_ordering(sort_by)
        tasks = Task.objects.all().order_by(*ordering)
        return render(request, self.template_name, {"tasks": tasks})

    def get_ordering(self, sort_by):
        ordering_mapping = {
            "completed": ("-completed", "created_at"),
            "created_at": ("created_at",),
            "worker": ("worker",),
            "created_by": ("created_by",),
            "deadline": ("deadline",),
        }
        return ordering_mapping.get(sort_by, ("created_at",))


class TaskListViewBase(ListView):
    model = Task
    template_name = None
    context_object_name = "tasks"

    def get_queryset(self):
        return self.model.objects.all()

    def apply_sorting(self, queryset, sort_by):
        sort_mapping = {
            "completed": ("-completed", "created_at"),
            "created_at": ("created_at",),
            "worker": ("worker",),
            "created_by": ("created_by",),
            "deadline": ("deadline",),
        }
        return queryset.order_by(*sort_mapping.get(sort_by, ("created_at",)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get("sort_by", "created_at")
        context["tasks"] = self.apply_sorting(context["tasks"], sort_by)
        return context


class AllTasks(LoginRequiredMixin, TaskListViewBase):
    template_name = "tasks/all_tasks.html"


class TasksFromMe(LoginRequiredMixin, TaskListViewBase):
    template_name = "tasks/from_me_tasks.html"

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class TasksForMe(LoginRequiredMixin, TaskListViewBase):
    template_name = "tasks/for_me_tasks.html"

    def get_queryset(self):
        return Task.objects.filter(worker=self.request.user)


# @method_decorator(login_required(login_url='/users/login/'), name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_execution_form"] = TaskExecutionForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        return redirect("tasks:task_detail", pk=task.pk)


class TaskCreateView(LoginRequiredMixin, CreateView):
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
class TaskUpdateView(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = "tasks/task_create.html"

    def get_success_url(self):
        return reverse("tasks:index")


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("tasks:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:index")


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
class UpdateTaskExecution(UpdateView):
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
