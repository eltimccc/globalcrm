from django.urls import path
from cars.views import CarCreateView, CarEditView, CarIndexView, CarDetailView


app_name = "cars"

urlpatterns = [
    path("", CarIndexView.as_view(), name="cars_index"),
    path('create/', CarCreateView.as_view(), name='create_car'),
    path('edit/<int:pk>/', CarEditView.as_view(), name='edit_car'),
    path('<int:pk>/', CarDetailView.as_view(), name='car_detail'),
]
