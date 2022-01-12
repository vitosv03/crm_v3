from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Apps.crm_app.models import InterPlaysList
from Apps.crm_app.filters import InterplaysFilter


class InterplayListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Rendering list of all Interplays
    """
    model = InterPlaysList
    template_name = 'crm_app/interplay/interplays_list.html'
    context_object_name = 'interplays'
    filterset_class = InterplaysFilter
    paginate_by = 10
    permission_required = 'crm_app.view_interplayslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplays List'
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct().select_related('created_by', 'project').prefetch_related('tag')


class InterplayDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Rendering list detail info about of one Interplay
    """
    model = InterPlaysList
    template_name = 'crm_app/interplay/interplay_detail.html'
    context_object_name = 'interplay'
    permission_required = 'crm_app.view_interplayslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail of:  ' + str(context['interplay'])
        context['owner'] = self.object.created_by == self.request.user
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('created_by').prefetch_related('tag')


class InterplayAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Rendering form to add a new Interplay
    """
    model = InterPlaysList
    context_object_name = 'interplay'
    template_name = 'crm_app/interplay/interplay_add.html'
    success_url = reverse_lazy('interplay_list')
    fields = ['project', 'link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.add_interplayslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new Interplay'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class InterplayUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Rendering form to update a new Interplay
    """
    model = InterPlaysList
    context_object_name = 'interplay'
    template_name = 'crm_app/interplay/interplay_update.html'
    fields = ['is_active', 'link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.change_interplayslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update of: '  + str(context['interplay'])
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset().select_related('created_by').prefetch_related('tag')
        return qs.filter(created_by=self.request.user)


class InterplayDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Rendering form to delete Interplay
    """
    model = InterPlaysList
    template_name = 'crm_app/interplay/interplay_delete.html'
    context_object_name = 'interplay'
    success_url = reverse_lazy('interplay_list')
    permission_required = 'crm_app.delete_interplayslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete of: ' + str(context['interplay'])
        return context

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
