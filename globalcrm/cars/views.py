from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.db.models import Q

from cars.models import Car
from cars.forms import CarCreateForm, CarEditForm
from .filters import CarFilter


class CarIndexView(ListView):
    template_name = "cars/cars_index.html"
    model = Car
    context_object_name = "cars"
    ordering = "model"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")

        filter = CarFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs

        if search_query:
            queryset = queryset.filter(
                Q(license_plate__icontains=search_query)
            )

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "model")
        return context


class CarCreateView(FormView):
    template_name = "cars/create_car.html"
    form_class = CarCreateForm
    success_url = reverse_lazy("cars:cars_index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CarEditView(UpdateView):
    model = Car
    form_class = CarEditForm
    template_name = "cars/car_edit.html"

    def get_success_url(self):
        return reverse_lazy("cars:cars_index")


class CarDetailView(DetailView):
    model = Car
    template_name = "cars/car_detail.html"
    context_object_name = "car"


class CarDeleteView(DeleteView):
    model = Car
    template_name = "cars/delete_car.html"
    success_url = reverse_lazy("cars:cars_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["car"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("cars:cars_index")


class CarModalView(View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        data = {'car': car}
        html_modal_content = render_to_string('cars/modal/car_modal.html', data)
        return JsonResponse({'html_modal_content': html_modal_content})
