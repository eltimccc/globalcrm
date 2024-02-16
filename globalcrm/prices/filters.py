import django_filters
from .models import Price


class ClientFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("tarif_name", "Имени"),
        ("price_15_30_days", "Цене 15-30"),
    )

    sort_by = django_filters.ChoiceFilter(
        field_name="__sort_by",
        label="Сортировать по:",
        choices=SORT_CHOICES,
        method="sort_by_filter",
    )

    def sort_by_filter(self, queryset, name, value):
        if value == "tarif_name":
            return queryset.order_by("tarif_name")
        elif value == "price_15_30_days":
            return queryset.order_by("price_15_30_days")

    class Meta:
        model = Price
        fields = []
