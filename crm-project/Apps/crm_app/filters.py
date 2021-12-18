import django_filters
from django import forms

from .models import ClientsInfo, ProjectsList, InterPlaysList


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

    # client = django_filters.ModelChoiceFilter(
    #     label='Client',
    #     queryset=ClientsInfo.objects.filter(projectslist__pk__in=q_set),
    #     # method='filter_by_client',
    #     widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    # )

    class Meta:
        model = ProjectsList
        fields = ['project', 'client']

    # def filter_by_client(self, queryset, name, value):
    #     q_set = ProjectsList.objects.filter(client=value).values_list('id', flat=True)[0]
    #     return queryset.filter(project_id=q_set)

