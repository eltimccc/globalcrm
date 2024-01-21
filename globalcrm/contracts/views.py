from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Contract
from .forms import ContractForm

class ContractListView(ListView):
    model = Contract
    template_name = 'contracts/contract_index.html'
    context_object_name = 'contracts'

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_create.html'
    success_url = '/contracts/list/'
