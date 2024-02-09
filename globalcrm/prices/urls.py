from django.urls import path
from prices.views import (
    PriceCreateView,
    PriceDeleteView,
    PriceEditView,
    PriceIndexView,
    PriceDetailView,
)


app_name = "prices"

urlpatterns = [
    path("", PriceIndexView.as_view(), name="prices_index"),
    path("create/", PriceCreateView.as_view(), name="create_price"),
    path("edit/<int:pk>/", PriceEditView.as_view(), name="edit_price"),
    path("<int:pk>/", PriceDetailView.as_view(), name="detail_price"),
    path("delete/<int:pk>/", PriceDeleteView.as_view(), name="delete_price"),
]
