import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Client

# from .forms import TaskForm, UpdateTaskForm
from django.utils import timezone
from django.utils.timezone import make_aware


class IndexView(TemplateView):
    template_name = "clients/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = Client.objects.all()
        return context
