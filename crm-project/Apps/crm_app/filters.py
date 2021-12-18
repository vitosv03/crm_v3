import django_filters
from django import forms
from django.views.generic import ListView

from .models import ClientsInfo


class ClientsInfoFilter(django_filters.FilterSet):
    CHOICES = (
        ('by title acs', 'title acs'),
        ('by title desc', 'title desc'),
        ('by date_created acs', 'created acs'),
        ('by date_created desc', 'created desc'),
    )
    sort = django_filters.ChoiceFilter(
        label='Sort by',
        choices=CHOICES,
        method='filter_by_order',
        widget=forms.Select(attrs={'onchange' : "this.form.submit()"})
    )

    class Meta:
        model = ClientsInfo
        # fields = {'title': ['icontains'], }
        # fields = dict(title=['icontains'],)
        fields = ['sort', ]

    def filter_by_order(self, queryset, name, value):
        # title_sort = 'title' if value == 'asc' else '-title'
        # global sorting
        if value == 'by title acs':
            sorting = 'title'
        elif value == 'by title desc':
            sorting = '-title'
        elif value == 'by date_created acs':
            sorting = 'date_created'
        elif value == 'by date_created desc':
            sorting = '-date_created'
        print(sorting)
        return queryset.order_by(sorting)


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
