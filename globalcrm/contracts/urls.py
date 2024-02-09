from django.urls import path
from .views import (
    ContractDeleteView,
    ContractDetailView,
    ContractEditView,
    ContractListView,
    ContractCreateView,
    calculate_price_ajax,
    get_car_tariff,
    get_end_date,
)


app_name = "contracts"

urlpatterns = [
    path("list/", ContractListView.as_view(), name="contract_index"),
    path("create/", ContractCreateView.as_view(), name="contract_create"),
    path("edit/<int:pk>/", ContractEditView.as_view(), name="contract_edit"),
    path("get_car_tariff/", get_car_tariff, name="get_car_tariff"),
    path("get_end_date/", get_end_date, name="get_end_date"),
    path("calculate_price/", calculate_price_ajax, name="calculate_price"),
    path("<int:pk>/", ContractDetailView.as_view(), name="contract_detail"),
    path("<int:pk>/delete/", ContractDeleteView.as_view(), name="contract_delete"),
]
