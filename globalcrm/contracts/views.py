from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from cars.models import Car
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

    def form_valid(self, form):
        form.instance.tariff_id = self.request.POST.get('tariff')
        return super().form_valid(form)


def get_car_tariff(request):
    car_id = request.GET.get('car_id')
    try:
        car = Car.objects.get(pk=car_id)
        tariff = car.tariff
        tariff = tariff.pk
        return JsonResponse({'tariff': tariff})
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Автомобиль не найден'}, status=404)
