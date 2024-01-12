from django.urls import path
from cars.views import CarIndexView


app_name = "cars"

urlpatterns = [
    path("", CarIndexView.as_view(), name="cars_index"),
    # path('create/', ClientCreateView.as_view(), name='create_client'),
    # path('edit/<int:client_id>/', ClientEditView.as_view(), name='edit_client'),
    # path('<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
]
