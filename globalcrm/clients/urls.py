from django.urls import path
from .views import CreateClientView, IndexView


app_name = "clients"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('create/', CreateClientView.as_view(), name='create_client'),
]
