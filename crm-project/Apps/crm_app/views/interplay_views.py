from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import InterPlaysList
from ..filters import InterplaysFilter


class InterplayListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = InterPlaysList
    # login_url = reverse_lazy('login')
    template_name = 'crm_app/interplay/interplays_list.html'
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
    template_name = 'crm_app/interplay/interplay_detail.html'
    context_object_name = 'interplay'
    permission_required = 'crm_app.view_interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail of:  ' + str(context['interplay'])
        return context


class InterplayAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = InterPlaysList
    context_object_name = 'interplay'
    template_name = 'crm_app/interplay/interplay_add.html'
    success_url = reverse_lazy('interplay_list')
    fields = ['project', 'link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.add_interplays'

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
    model = InterPlaysList
    context_object_name = 'interplay'
    template_name = 'crm_app/interplay/interplay_update.html'
    fields = ['link', 'description', 'rating', 'tag', ]
    permission_required = 'crm_app.change_interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update of: '  + str(context['interplay'])
        # obj = get_object_or_404(InterPlaysList, created_by=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class InterplayDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = InterPlaysList
    template_name = 'crm_app/interplay/interplay_delete.html'
    context_object_name = 'interplay'
    success_url = reverse_lazy('interplay_list')
    permission_required = 'crm_app.delete_interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete of: ' + str(context['interplay'])
        return context

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
