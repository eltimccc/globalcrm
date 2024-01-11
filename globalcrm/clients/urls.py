from django.urls import path
from .views import ClientDetailView, CreateClientView, IndexView, EditClientView


app_name = "clients"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('create/', CreateClientView.as_view(), name='create_client'),
    path('edit/<int:client_id>/', EditClientView.as_view(), name='edit_client'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
