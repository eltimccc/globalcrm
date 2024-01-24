from datetime import datetime, timedelta
from django.utils import timezone
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
    
    def calculate_price(self, contract):
        tariff = contract.tariff
        rental_days = contract.rental_days

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

        end_date = contract.start_date + timedelta(days=rental_days)

        return amount, end_date
    
    def form_valid(self, form):
        contract = form.save(commit=False)

        contract.amount, contract.end_date = self.calculate_price(contract)
        
        contract.save()
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


def get_end_date(request):
    try:
        rental_days = int(request.GET.get('rental_days', 0))
        
        start_date_str = request.GET.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')

        end_date = start_date + timezone.timedelta(days=rental_days)
        
        return JsonResponse({'end_date': end_date.strftime('%Y-%m-%d %H:%M:%S')})
    except Exception as e:
        import traceback
        traceback.print_exc()  # Выводим трассировку стека в консоль
        return JsonResponse({'error': str(e)}, status=500)


