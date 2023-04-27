from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from .forms import TaskForm


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
    template_name = 'tasks/task_form.html'
    fields = ['worker', 'content']


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
