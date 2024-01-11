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

from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic.edit import FormView


class IndexView(TemplateView):
    template_name = "clients/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all()
        return context


class CreateClientView(FormView):
    template_name = 'clients/create_client.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class EditClientView(View):
    template_name = 'clients/create_client.html'

    def get(self, request, client_id, *args, **kwargs):
        return render(
            request, self.template_name,
                      {'form': ClientForm(instance=Client.objects.get(pk=client_id))}
                      )

    def post(self, request, client_id, *args, **kwargs):
        client = Client.objects.get(pk=client_id)
        form = ClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()
            return redirect('clients:index')

        return render(request, self.template_name, {'form': form})
    

class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'