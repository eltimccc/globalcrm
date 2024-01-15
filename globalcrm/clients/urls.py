from django.urls import path
from .views import ClientDetailView, ClientCreateView, ClientIndexView, ClientEditView


app_name = "clients"

urlpatterns = [
    path("", ClientIndexView.as_view(), name="index"),
    path('create/', ClientCreateView.as_view(), name='create_client'),
    path('edit/<int:pk>/', ClientEditView.as_view(), name='edit_client'),
    path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
