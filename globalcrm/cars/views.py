from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from cars.models import Car

# Create your views here.
class CarIndexView(TemplateView):
    template_name = "cars/cars_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Car.objects.all()
        return context