import django_filters
from django import forms

from .models import ClientsInfo, ProjectsList, InterPlaysList, Tags
from django.contrib.auth import get_user_model


class ClientsInfoFilter(django_filters.FilterSet):
    sort = django_filters.OrderingFilter(
        label='Sort by',
        fields=(
            'title',
            'date_created',
        ),
        choices=(
            ('title', 'title_acs'),
            ('-title', 'title_desc'),
            ('date_created', 'created_acs'),
            ('-date_created', 'created_desc'),
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


class InterplaysFilter(django_filters.FilterSet):
    Users = get_user_model()

    qs_project = set(InterPlaysList.objects.values_list('project', flat=True))
    qs_tag = set(InterPlaysList.objects.values_list('tag', flat=True))
    qs_created_by = set(InterPlaysList.objects.values_list('created_by', flat=True))

    project = django_filters.ModelChoiceFilter(
        label='Project',
        queryset=ProjectsList.objects.filter(pk__in=qs_project),
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    client = django_filters.ModelChoiceFilter(
        label='Client',
        queryset=ClientsInfo.objects.filter(projectslist__pk__in=qs_project),
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    created_by = django_filters.ModelChoiceFilter(
        label='Created_by',
        queryset=Users.objects.filter(pk__in=qs_created_by),
        widget=forms.Select(attrs={'onchange': "this.form.submit()"})
    )

    sort = django_filters.OrderingFilter(
        label='Sort by',
        fields=(
            'client',
            'project',
            'date_created',
            'created_by',
        ),
        choices=(
            ('client', 'client_acs'),
            ('-client', 'client_desc'),
            ('project', 'project_acs'),
            ('-project', 'project_desc'),
            ('created_by', 'created_acs'),
            ('-created_by', 'created_desc'),
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
        queryset=Tags.objects.filter(id__in=qs_tag),
        widget=forms.SelectMultiple(attrs={
            'onchange': "this.form.submit()",
            'class': "select_field_class",
            'style': "width:500px"
        }
        ),
    )

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #     super(InterplaysFilter, self).__init__(*args, **kwargs)

    # my_records = django_filters.ModelMultipleChoiceFilter(
    #     lookup_expr='exact',
    #     queryset=ProjectsList.objects.filter(created_by=request.user),
    #
    # )

    class Meta:
        model = ProjectsList
        fields = ['project', 'client', 'sort', 'created_by', 'tag']
