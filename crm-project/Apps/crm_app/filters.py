import django_filters
from django import forms

from .models import ClientsInfo, ProjectsList, InterPlaysList
from .utils import SORT_CHOICES_InterplaysFilter, SORT_CHOICES_ClientsInfoFilter


class ClientsInfoFilter(django_filters.FilterSet):

    sort = django_filters.ChoiceFilter(
        label='Sort by',
        choices=SORT_CHOICES_ClientsInfoFilter,
        method='filter_by_order',
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    class Meta:
        model = ClientsInfo
        fields = ['sort', ]

    def filter_by_order(self, queryset, name, value):
        if value == 'title_acs':
            sorting = 'title'
        elif value == 'title_desc':
            sorting = '-title'
        elif value == 'created_acs':
            sorting = 'date_created'
        elif value == 'created_desc':
            sorting = '-date_created'
        return queryset.order_by(sorting)


class InterplaysFilter(django_filters.FilterSet):
    q_set = InterPlaysList.objects.values_list('project')

    project = django_filters.ModelChoiceFilter(
        label='Project',
        queryset=ProjectsList.objects.filter(pk__in=q_set),
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    client = django_filters.ModelChoiceFilter(
        label='Client',
        queryset=ClientsInfo.objects.filter(projectslist__pk__in=q_set),
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    sort = django_filters.ChoiceFilter(
        label='Sort by',
        choices=SORT_CHOICES_InterplaysFilter,
        method='filter_by_order',
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    def filter_by_order(self, queryset, name, value):
        if value == 'client_acs':
            sorting = 'client'
        elif value == 'client_desc':
            sorting = '-client'
        elif value == 'project_acs':
            sorting = 'project'
        elif value == 'project_desc':
            sorting = '-project'
        elif value == 'created_acs':
            sorting = 'date_created'
        elif value == 'created_desc':
            sorting = '-date_created'
        return queryset.order_by(sorting)


    class Meta:
        model = ProjectsList
        fields = ['project', 'client', 'sort', ]


