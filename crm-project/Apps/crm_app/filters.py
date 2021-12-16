import django_filters

from .models import ClientsInfo


class ClientsInfoFilter(django_filters.FilterSet):

    class Meta:
        model = ClientsInfo
        fields = {
            'title': ['icontains'],

        }

