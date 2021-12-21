from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import InterPlaysList
from ..filters import InterplaysFilter


class InterplayListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InterPlaysList
    template_name = 'interplay/interplays_list.html'
    context_object_name = 'interplays'
    filterset_class = InterplaysFilter
    paginate_by = 10
    permission_required = 'crm_app.view_interplays'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplays List'
        context['filter'] = self.filterset
        # print(self.request.user)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct().select_related('created_by')


class InterplayDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = InterPlaysList
    template_name = 'interplay/interplay_detail.html'
    context_object_name = 'interplay'
    permission_required = 'crm_app.view_interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplay: ' + str(context['interplay'])
        return context


class InterplayAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = InterPlaysList
    template_name = 'interplay/interplay_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['project', 'link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.add_interplays'

    # def __init__(self, *args, **kwargs):
    #     super(InterplaysAddView, self).__init__(self, *args, **kwargs)
    #     # self.fields['description'].queryset = Project.objects.filter(Project.status == 2)
    #     self.field['description'] = 'dfd'

    # def get_initial(self, *args, **kwargs):
    #     initial = super(InterplaysAddView, self).get_initial(**kwargs)
    #     data = self.request.GET.get('data')
    #     if data is not None:
    #         print(data)
    #         self.initial['project'] = data
    #     return initial
    #
    # def get_initial(self, *args, **kwargs):
    #     initial = super(InterplaysAddView, self).get_initial(**kwargs)
    #     # data = self.request.GET.get('data')
    #     # if data is not None:
    #     #     print(data)
    #     self.initial['description']  = self.id
    #     return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        # edit_form.client = ClientsInfo.objects.filter(projectslist__p_name='ddf')[0]
        self.object = form.save()
        return super().form_valid(form)


class InterplayUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = InterPlaysList
    template_name = 'interplay/interplay_update.html'
    # success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.change_interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class InterplayDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = InterPlaysList
    template_name = 'interplay/interplay_delete.html'
    context_object_name = 'interplay'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_interplays'
