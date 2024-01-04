import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from clients.forms import ClientForm
from .models import Client

# from .forms import TaskForm, UpdateTaskForm
from django.utils import timezone
from django.utils.timezone import make_aware


class IndexView(TemplateView):
    template_name = "clients/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all()
        return context


class CreateClientView(View):
    template_name = 'clients/create_client.html'

    def get(self, request, *args, **kwargs):
        form = ClientForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('clients:index')

        return render(request, self.template_name, {'form': form})