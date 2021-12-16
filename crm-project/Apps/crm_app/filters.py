from random import choices

import django_filters

from .models import ClientsInfo


class ClientsInfoFilter(django_filters.FilterSet):
    CHOICES = (
        ('asc', 'asc'),
        ('desc', 'desc'),
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = ClientsInfo
        fields = {
            'title': ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        title_sort = 'title' if value == 'asc' else '-title'
        return queryset.order_by(title_sort)
