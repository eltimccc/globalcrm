from django import forms
from .models import Car


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'registration_date': forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}),
        }
        input_formats = ['%d.%m.%Y']