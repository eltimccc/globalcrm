import django_filters
from .models import Client


class ClientFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("surname", "Фамилии"),
        ("name", "Имени"),
    )

    sort_by = django_filters.ChoiceFilter(
        field_name="__sort_by",
        label="Сортировать по:",
        choices=SORT_CHOICES,
        method="sort_by_filter",
    )

    def sort_by_filter(self, queryset, name, value):
        if value == "surname":
            return queryset.order_by("surname")
        elif value == "name":
            return queryset.order_by("name")

    class Meta:
        model = Client
        fields = []
