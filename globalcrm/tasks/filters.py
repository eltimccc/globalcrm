import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ("created_at", "Дате создания"),
        ("completed", "Статусу"),
        ("worker", "Исполнителю"),
        ("created_by", "Заказчику"),
        ("deadline", "Дедлайну"),
    )

    sort_by = django_filters.ChoiceFilter(
        field_name="__sort_by",
        label="Сортировать по:",
        choices=SORT_CHOICES,
        method="sort_by_filter",
    )

    def sort_by_filter(self, queryset, name, value):
        if value == "completed":
            return queryset.order_by("-completed", "created_at")
        elif value == "worker":
            return queryset.order_by("worker", "created_at")
        elif value == "created_by":
            return queryset.order_by("created_by", "created_at")
        elif value == "deadline":
            return queryset.order_by("deadline", "created_at")
        else:
            return queryset.order_by("created_at")

    class Meta:
        model = Task
        fields = []
