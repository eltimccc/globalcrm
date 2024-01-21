from django import forms
from .models import Contract

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'  # Все поля модели Contract
        labels = {
            'client': 'Клиент',
            'car': 'Автомобиль',
            'tariff': 'Тариф',
            'start_date': 'Начальная дата',
            'end_date': 'Конечная дата',
            'rental_days': 'Количество суток аренды',
            'amount': 'Стоимость аренды',
        }