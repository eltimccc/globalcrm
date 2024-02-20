import django_filters
from .models import Contract


class ContractFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("id", "ID"),
        ("start_date", "Началу договора"),
        ("client", "Клиенту"),
        ("car", "Машине"),
    )

    sort_by = django_filters.ChoiceFilter(
        field_name="__sort_by",
        label="Сортировать по:",
        choices=SORT_CHOICES,
        method="sort_by_filter",
    )

    def sort_by_filter(self, queryset, name, value):
        if value == "start_date":
            return queryset.order_by("start_date")
        elif value == "id":
            return queryset.order_by("id")
        elif value == "client":
            return queryset.order_by("client")
        elif value == "car":
            return queryset.order_by("car")

    class Meta:
        model = Contract
        fields = []
