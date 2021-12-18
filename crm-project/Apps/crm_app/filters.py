import django_filters
from django import forms
from django.views.generic import ListView

from .models import ClientsInfo


class ClientsInfoFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('title_acs', 'title acs'),
        ('title_desc', 'title desc'),
        ('created_acs', 'created acs'),
        ('created_desc', 'created desc'),
    )
    sort = django_filters.ChoiceFilter(
        label='Sort by',
        choices=SORT_CHOICES,
        method='filter_by_order',
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    class Meta:
        model = ClientsInfo
        # fields = {'title': ['icontains'], }
        # fields = dict(title=['icontains'],)
        fields = ['sort', ]

    def filter_by_order(self, queryset, name, value):
        # title_sort = 'title' if value == 'asc' else '-title'
        # global sorting
        if value == 'title_acs':
            sorting = 'title'
        elif value == 'title_desc':
            sorting = '-title'
        elif value == 'created_acs':
            sorting = 'date_created'
        elif value == 'created_desc':
            sorting = '-date_created'
        # print(sorting)
        return queryset.order_by(sorting)


# class FilteredListView(ListView):
#     # model = ClientsInfo
#     filterset_class = None
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
#         return self.filterset.qs.distinct()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context



# -------------------------------------------------
# class ClientFilterSet(django_filters.FilterSet):
#     def __init__(self, data, *args, **kwargs):
#         data = data.copy()
#         # data.setdefault('format', 'paperback')
#         data.setdefault('ClientsInfo', '-title')
#         super().__init__(data, *args, **kwargs)
