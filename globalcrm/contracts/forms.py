from django import forms
from .models import Contract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        labels = {
            'client': 'Клиент',
            'car': 'Автомобиль',
            'tariff': 'Тариф',
            'start_date': 'Начальная дата',
            'end_date': 'Конечная дата',
            'rental_days': 'Количество суток аренды',
            'amount': 'Стоимость аренды',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Создать договор'))