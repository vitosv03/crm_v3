from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import ProjectsList
from ..filters import ProjectsListFilter

class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProjectsList
    template_name = 'crm_app/project/projects_list.html'
    context_object_name = 'projects'
    filterset_class = ProjectsListFilter
    permission_required = 'crm_app.view_projectslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects List'
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct().select_related('created_by')

class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ProjectsList
    template_name = 'crm_app/project/project_detail.html'
    context_object_name = 'project'
    permission_required = 'crm_app.view_projectslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail of: ' + str(context['project'])
        return context


class ProjectAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProjectsList
    context_object_name = 'project'
    template_name = 'crm_app/project/project_add.html'
    success_url = reverse_lazy('project_list')
    fields = ['client', 'p_name', 'description', 'date_begin', 'date_end', 'value', ]
    permission_required = 'crm_app.add_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new Project'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProjectsList
    context_object_name = 'project'
    template_name = 'crm_app/project/project_update.html'
    fields = ['client', 'p_name', 'description',
              'date_begin', 'date_end', 'value', ]
    permission_required = 'crm_app.change_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update of: ' + str(context['project'])
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProjectsList
    template_name = 'crm_app/project/project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project_list')
    permission_required = 'crm_app.delete_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete of: ' + str(context['project'])
        return context

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
