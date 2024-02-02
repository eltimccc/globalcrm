from django import forms
from .models import Client
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'patronomic': 'Отчество',
            'birth_date': 'Дата рождения',
            'passport_series_number': 'Серия и номер паспорта',
            'passport_issue_date': 'Дата выдачи паспорта',
            'passport_issued_by': 'Кем выдан паспорт',
            # 'country': 'Страна',
            # 'city': 'Город',
            'address': 'Улица, дом, квартира',
            'driving_number': 'Номер водительского удостоверения',
            'driver_license_issue_date': 'Дата выдачи водительского удостоверения',
            'driver_license_valid_until': 'Действительно до',
            'email': 'Электронная почта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Добавить клиента'))