from django import forms
from .models import Car
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
        widgets = {
            "registration_date": forms.TextInput(attrs={"placeholder": "YYYY-DD-MM"}),
        }
        input_formats = ["%d.%m.%Y"]
        labels = {
            "model": "Модель автомобиля",
            "license_plate": "Номерной знак",
            "year": "Год выпуска",
            "color": "Цвет",
            "registration_number": "Номер СТС",
            "registration_date": "Дата регистрации",
            "tariff": "Тариф автомобиля",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.add_input(Submit("submit", "Добавить автомобиль"))


class CarEditForm(CarCreateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Сохранить изменения"))
