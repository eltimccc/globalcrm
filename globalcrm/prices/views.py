from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)
from django.urls import reverse_lazy

from prices.models import Tariff
from prices.forms import PriceCreateForm


# class PriceIndexView(TemplateView):
#     template_name = "prices/prices_index.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["prices"] = Tariff.objects.all()
#         return context


class PriceIndexView(ListView):
    template_name = "prices/prices_index.html"
    model = Tariff
    context_object_name = "prices"
    ordering = "price_15_30_days"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(self.request.GET.get("sort_by", self.ordering))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", self.ordering)
        return context


class PriceCreateView(FormView):
    template_name = "prices/create_price.html"
    form_class = PriceCreateForm
    success_url = reverse_lazy("prices:prices_index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PriceEditView(UpdateView):
    template_name = "prices/edit_price.html"
    form_class = PriceCreateForm
    model = Tariff

    def get_success_url(self):
        return reverse_lazy("prices:prices_index")


class PriceDetailView(DetailView):
    model = Tariff
    template_name = "prices/price_detail.html"
    context_object_name = "price"


class PriceDeleteView(DeleteView):
    model = Tariff
    template_name = "prices/delete_price.html"
    success_url = reverse_lazy("prices:prices_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["price"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("prices:prices_index")
