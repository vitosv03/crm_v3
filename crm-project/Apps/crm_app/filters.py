import django_filters
from django.views.generic import ListView

from .models import ClientsInfo


class ClientsInfoFilter(django_filters.FilterSet):
    CHOICES = (
        ('by title acs', 'title acs'),
        ('by title desc', 'title desc'),
        ('by date_created acs', 'date_created acs'),
        ('by date_created desc', 'date_created desc'),
    )
    ordering = django_filters.ChoiceFilter(label='Sort by', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = ClientsInfo
        # fields = {'title': ['icontains'], }
        # fields = dict(title=['icontains'],)
        fields = ['ordering', ]

    def filter_by_order(self, queryset, name, value):
        # title_sort = 'title' if value == 'asc' else '-title'
        if value == 'by title acs':
            title_sort = 'title'
        elif value == 'by title desc':
            title_sort = '-title'
        elif value == 'by date_created acs':
            title_sort = 'date_created'
        elif value == 'by date_created desc':
            title_sort = '-date_created'
        return queryset.order_by(title_sort)


class FilteredListView(ListView):
    model = ClientsInfo
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context

    # class Meta:
        # model = ClientsInfo
    #     fields = {
    #         'title': ['icontains'],
    #     }

# -------------------------------------------------
# class ClientFilterSet(django_filters.FilterSet):
#     def __init__(self, data, *args, **kwargs):
#         data = data.copy()
#         # data.setdefault('format', 'paperback')
#         data.setdefault('ClientsInfo', '-title')
#         super().__init__(data, *args, **kwargs)
