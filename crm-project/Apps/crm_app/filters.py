from urllib import request

import django_filters
from django import forms
from django.contrib.messages.storage import session
from django.forms import Select
from django_filters.widgets import LinkWidget, SuffixedMultiWidget, CSVWidget, LookupChoiceWidget, QueryArrayWidget

from .models import ClientsInfo, ProjectsList, InterPlaysList, Tags
from .utils import SORT_CHOICES_InterplaysFilter, SORT_CHOICES_ClientsInfoFilter


class ClientsInfoFilter(django_filters.FilterSet):
    sort = django_filters.OrderingFilter(
        label='Sort by',
        fields=('title', 'date_created', ),
        choices=(
            ('title', 'title_acs'), ('-title', 'title_desc'),
            ('date_created', 'created_acs'), ('-date_created', 'created_desc'),
         ),
        # field_labels={
        #     'title', 'title_acs',
        #     '-title', 'title_desc',
        #     'date_created', 'date_created',
        #     '-date_created', 'created_desc',
        # },
     )

    class Meta:
         model = ClientsInfo
         fields = ['sort', ]

# sort = django_filters.ChoiceFilter(
    #     label='Sort by',
    #     choices=SORT_CHOICES_ClientsInfoFilter,
    #     method='filter_by_order',
    #     widget=forms.Select(attrs={'onchange': "this.form.submit()"}))
    #
    # @staticmethod
    # def filter_by_order(queryset, name, value):
    #     if value == 'title_acs':
    #         sorting = 'title'
    #     elif value == 'title_desc':
    #         sorting = '-title'
    #     elif value == 'created_acs':
    #         sorting = 'date_created'
    #     elif value == 'created_desc':
    #         sorting = '-date_created'
    #     return queryset.order_by(sorting)


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

    sort = django_filters.OrderingFilter(
        label='Sort by',
        fields=('client',
                'project',
                'date_created',
                ),
        choices=(
            ('client', 'client_acs'),
            ('-client', 'client_desc'),
            ('project', 'project_acs'),
            ('-project', 'project_desc'),
            ('date_created', 'date_created'),
            ('-date_created', 'created_desc'),
         ),
        # field_labels={
        #     'client', 'client_acs',
        #     '-client', 'client_desc',
        #     'project', 'project_acs',
        #     '-project', 'project_desc',
        #     'date_created', 'date_created',
        #     '-date_created', 'created_desc',
        # },
    )

    # sort = django_filters.ChoiceFilter(
    #     label='Sort by',
    #     choices=SORT_CHOICES_InterplaysFilter,
    #     method='filter_by_order',
    #     widget=forms.Select(attrs={'onchange': "this.form.submit()"}))
    #
    # @staticmethod
    # def filter_by_order(queryset, name, value):
    #     if value == 'client_acs':
    #         sorting = 'client'
    #     elif value == 'client_desc':
    #         sorting = '-client'
    #     elif value == 'project_acs':
    #         sorting = 'project'
    #     elif value == 'project_desc':
    #         sorting = '-project'
    #     elif value == 'created_acs':
    #         sorting = 'date_created'
    #     elif value == 'created_desc':
    #         sorting = '-date_created'
    #     return queryset.order_by(sorting)

    tag = django_filters.ModelMultipleChoiceFilter(
        lookup_expr='exact',
        queryset=Tags.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'onchange': "this.form.submit()",
            'class': "select_field_class",
            'style': "width:500px"
        }),
    )

    class Meta:
        model = ProjectsList
        fields = ['project', 'client', 'sort', 'created_by', 'tag']


