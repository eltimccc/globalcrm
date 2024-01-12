from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from clients.forms import ClientForm
from .models import Client


class ClientIndexView(TemplateView):
    template_name = "clients/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clients"] = Client.objects.all()
        return context


class ClientCreateView(FormView):
    template_name = 'clients/create_client.html'
    form_class = ClientForm
    success_url = reverse_lazy('clients:index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class ClientEditView(View):
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