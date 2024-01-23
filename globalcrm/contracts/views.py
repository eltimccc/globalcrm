from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views.generic.edit import FormView

from cars.models import Car
from .models import Contract
from .forms import ContractForm

class ContractListView(ListView):
    model = Contract
    template_name = 'contracts/contract_index.html'
    context_object_name = 'contracts'


class ContractCreateView(FormView):
    model = Contract
    form_class = ContractForm
    template_name = 'contracts/contract_create.html'
    success_url = '/contracts/list/'
    
    def form_valid(self, form):
        contract = form.save(commit=False)

        # Вычисляем стоимость и обновляем end_date
        contract.amount, contract.end_date = self.calculate_price(contract)
        print('дада форме', contract.end_date)
        
        contract.save()
        return super().form_valid(form)
    
    def calculate_price(self, contract):
        # Получаем информацию о тарифе
        tariff = contract.tariff
        rental_days = contract.rental_days

        # Вычисляем стоимость в зависимости от количества дней аренды
        price_per_day = getattr(tariff, 'price_per_day', 0)
        price_2_3_days = getattr(tariff, 'price_2_3_days', 0)
        price_4_7_days = getattr(tariff, 'price_4_7_days', 0)
        price_8_14_days = getattr(tariff, 'price_8_14_days', 0)
        price_15_30_days = getattr(tariff, 'price_15_30_days', 0)

        if 2 <= rental_days <= 3:
            amount = price_2_3_days * rental_days
        elif 4 <= rental_days <= 7:
            amount = price_4_7_days * rental_days
        elif 8 <= rental_days <= 14:
            amount = price_8_14_days * rental_days
        elif 15 <= rental_days <= 30:
            amount = price_15_30_days * rental_days
        else:
            amount = price_per_day * rental_days

        # Обновляем end_date с учетом точного времени
        end_date = contract.start_date + timedelta(days=rental_days)
        print('перед ретюрн', end_date)

        return amount, end_date

def get_car_tariff(request):
    car_id = request.GET.get('car_id')
    try:
        car = Car.objects.get(pk=car_id)
        tariff = car.tariff
        tariff = tariff.pk
        return JsonResponse({'tariff': tariff})
    except Car.DoesNotExist:
        return JsonResponse({'error': 'Автомобиль не найден'}, status=404)
