from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import ProjectsList


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProjectsList
    template_name = 'project/projects_list.html'
    context_object_name = 'projects'
    permission_required = 'crm_app.view_projectslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects List'
        return context


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ProjectsList
    template_name = 'project/project_detail.html'
    context_object_name = 'project'
    permission_required = 'crm_app.view_projectslist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project: ' + str(context['project'])
        return context


class ProjectAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProjectsList
    template_name = 'project/project_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['client', 'p_name', 'description', 'date_begin', 'date_end', 'value', ]
    permission_required = 'crm_app.add_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ProjectsList
    template_name = 'project/project_update.html'
    # success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['client', 'p_name', 'description',
              'date_begin', 'date_end', 'value', ]
    permission_required = 'crm_app.change_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
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
    template_name = 'project/project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_projectlist'

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
