from django import forms
from .models import Tariff


class PriceCreateForm(forms.ModelForm):
    class Meta:
        model = Tariff
        fields = '__all__'
