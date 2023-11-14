from django.urls import path
from .views import IndexView


app_name = "clients"

urlpatterns = [
    path("", IndexView.as_view(), name="clients"),
]
