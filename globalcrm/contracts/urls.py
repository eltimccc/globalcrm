from django.urls import path
from .views import ContractListView, ContractCreateView

app_name = 'contracts'

urlpatterns = [
    path('list/', ContractListView.as_view(), name='contract_index'),
    path('create/', ContractCreateView.as_view(), name='contract_create'),
]
