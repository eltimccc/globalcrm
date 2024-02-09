from django import forms
from .models import Tariff
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class PriceCreateForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = "__all__"
        labels = {
            "tarif_name": "Название тарифа",
            "price_per_day": "Одни сутки",
            "price_2_3_days": "2-3 суток",
            "price_4_7_days": "4-7 суток",
            "price_8_14_days": "8-14 суток",
            "price_15_30_days": "15-30 суток",
            "deposit": "Залог",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.add_input(Submit("submit", "Добавить тариф"))
