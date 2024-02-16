from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView, DeleteView

from clients.forms import ClientForm
from .filters import ClientFilter
from .models import Client


class ClientIndexView(ListView):
    template_name = "clients/index.html"
    model = Client
    context_object_name = "clients"
    ordering = "surname"

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ClientFilter(self.request.GET, queryset=queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "surname")
        return context


class ClientCreateView(FormView):
    template_name = "clients/create_client.html"
    form_class = ClientForm
    success_url = reverse_lazy("clients:index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ClientEditView(UpdateView):
    template_name = "clients/edit_client.html"
    form_class = ClientForm
    model = Client

    def get_success_url(self):
        return reverse_lazy("clients:index")


class ClientDetailView(DetailView):
    model = Client
    template_name = "clients/client_detail.html"
    context_object_name = "client"


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/delete_client.html"
    success_url = reverse_lazy("clients:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("clients:index")
