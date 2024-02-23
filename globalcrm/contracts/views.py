from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    DeleteView,
    UpdateView,
)
from django.views.generic.edit import FormView
from django.views.decorators.http import require_GET
from django.db.models import Q

from cars.models import Car
from .filters import ContractFilter
from .models import Contract
from .forms import ContractForm
from prices.views import Tariff
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required(login_url="/users/login/"), name="dispatch")
class ContractListView(ListView):
    model = Contract
    template_name = "contracts/contract_index.html"
    context_object_name = "contracts"
    ordering = "id"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")

        filter = ContractFilter(self.request.GET, queryset=queryset)
        queryset = filter.qs

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query)
                | Q(client__name__icontains=search_query)
                | Q(client__surname__icontains=search_query)
            )

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "id")
        return context


def calculate_price(contract):
    tariff = contract.tariff
    rental_days = contract.rental_days

    price_per_day = tariff.price_per_day if hasattr(tariff, "price_per_day") else 0
    price_2_3_days = tariff.price_2_3_days if hasattr(tariff, "price_2_3_days") else 0
    price_4_7_days = tariff.price_4_7_days if hasattr(tariff, "price_4_7_days") else 0
    price_8_14_days = (
        tariff.price_8_14_days if hasattr(tariff, "price_8_14_days") else 0
    )
    price_15_30_days = (
        tariff.price_15_30_days if hasattr(tariff, "price_15_30_days") else 0
    )

    if 2 <= rental_days <= 3:
        amount = price_2_3_days * rental_days
    elif 4 <= rental_days <= 7:
        amount = price_4_7_days * rental_days
    elif 8 <= rental_days <= 14:
        amount = price_8_14_days * rental_days
    elif 15 <= rental_days:
        amount = price_15_30_days * rental_days
    else:
        amount = price_per_day * rental_days

    end_date = contract.start_date + timedelta(days=rental_days)

    return {"amount": amount, "end_date": end_date}


@require_GET
def calculate_price_ajax(request):
    try:
        tariff_id = request.GET.get("tariff_id")
        rental_days = request.GET.get("rental_days")

        try:
            tariff = Tariff.objects.get(pk=tariff_id)
        except Tariff.DoesNotExist:
            return JsonResponse({"error": "Invalid tariff ID"})

        try:
            rental_days = int(rental_days)
        except ValueError:
            return JsonResponse({"error": "Invalid rental days"})

        contract = Contract(tariff=tariff, rental_days=rental_days)

        result = calculate_price(contract)

        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def get_end_date(request):
    try:
        rental_days = int(request.GET.get("rental_days", 0))
        start_date_str = request.GET.get("start_date")

        if start_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
            end_date = start_date + timedelta(days=rental_days)

            return JsonResponse({"end_date": end_date.strftime("%Y-%m-%d %H:%M:%S")})
        else:
            return JsonResponse({"error": "Invalid start_date"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


class ContractCreateView(FormView):
    model = Contract
    form_class = ContractForm
    template_name = "contracts/contract_create.html"
    success_url = "/contracts/list/"

    def form_valid(self, form):
        contract = form.save(commit=False)

        result = calculate_price(contract)
        contract.amount = result["amount"]
        contract.end_date = result["end_date"].strftime("%Y-%m-%d %H:%M:%S")

        contract.save()
        return super().form_valid(form)


def get_car_tariff(request):
    car_id = request.GET.get("car_id")
    try:
        car = Car.objects.get(pk=car_id)
        tariff = car.tariff
        tariff = tariff.pk
        return JsonResponse({"tariff": tariff})
    except Car.DoesNotExist:
        return JsonResponse({"error": "Автомобиль не найден"}, status=404)


class ContractDetailView(DetailView):
    model = Contract
    template_name = "contracts/contract_detail.html"
    context_object_name = "contract"


class ContractDeleteView(DeleteView):
    model = Contract
    template_name = "contracts/contract_delete.html"
    success_url = reverse_lazy("contracts:contract_index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contract"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("contracts:contract_index")


class ContractEditView(UpdateView):
    template_name = "contracts/contract_edit.html"
    form_class = ContractForm
    model = Contract

    def get_success_url(self):
        return reverse_lazy("contracts:contract_index")
