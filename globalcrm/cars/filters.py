import django_filters
from .models import Car

class CarFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('model', 'Модели автомобиля'),
        ('year', 'Году выпуска'),
        ('license_plate', 'Регистрационному знаку'),
    )

    sort_by = django_filters.ChoiceFilter(
        field_name='__sort_by',
        label='Сортировать по:',
        choices=SORT_CHOICES,
        method='sort_by_filter'
    )

    def sort_by_filter(self, queryset, name, value):
        if value == 'model':
            return queryset.order_by('model')
        elif value == 'year':
            return queryset.order_by('-year')
        elif value == 'license_plate':
            return queryset.order_by('license_plate')

    class Meta:
        model = Car
        fields = []