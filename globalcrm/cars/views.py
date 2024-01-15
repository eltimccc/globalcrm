from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy

from cars.models import Car
from cars.forms import CarCreateForm


class CarIndexView(TemplateView):
    template_name = "cars/cars_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Car.objects.all()
        return context


class CarCreateView(FormView):
    template_name = 'cars/create_car.html'
    form_class = CarCreateForm
    success_url = reverse_lazy('cars:cars_index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class CarEditView(UpdateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'cars/create_car.html'
    success_url = reverse_lazy('cars:cars_index')


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'