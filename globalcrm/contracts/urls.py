from django.urls import path
from .views import ContractListView, ContractCreateView, get_car_tariff, get_end_date


app_name = 'contracts'

urlpatterns = [
    path('list/', ContractListView.as_view(), name='contract_index'),
    path('create/', ContractCreateView.as_view(), name='contract_create'),
    path('get_car_tariff/', get_car_tariff, name='get_car_tariff'),
    path('get_end_date/', get_end_date, name='get_end_date'),
]
