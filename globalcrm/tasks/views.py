import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UpdateTaskForm
from django.utils import timezone
from django.utils.timezone import make_aware



class IndexView(TemplateView):
    template_name = 'tasks/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greeting'] = 'Привет!'
        context['tasks'] = Task.objects.all()
        return context
    
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.completed = not task.completed
        task.save()
        return redirect('tasks:task_detail', pk=task.pk)


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks:index')
    

class UpdateTaskView(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = 'tasks/task_form.html'

    def get_success_url(self):
        return reverse('tasks:index')


class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy('tasks:index')





class Profile(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/profile.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'completed':
            context['tasks'] = sorted(context['tasks'], key=lambda x: x.completed)
        elif sort_by == 'created':
            context['tasks'] = sorted(context['tasks'], key=lambda x: x.created_at )

        return context
