from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Apps.crm_app.models import Tags


class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Rendering list of all tags
    """
    model = Tags
    template_name = 'crm_app/tag/tags_list.html'
    context_object_name = 'tags'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags List'
        return context


class TagDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Rendering list detail info about of one tag
    """
    model = Tags
    template_name = 'crm_app/tag/tag_detail.html'
    context_object_name = 'tag'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail of:  ' + str(context['tag'])
        context['owner'] = self.object.created_by == self.request.user
        return context


class TagAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Rendering form to add a new tag
    """
    model = Tags
    template_name = 'crm_app/tag/tag_add.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('tag_list')
    fields = ['tag']
    permission_required = 'crm_app.add_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new Tag'
        return context


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Rendering form to update a new tag
    """
    model = Tags
    template_name = 'crm_app/tag/tag_add.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('home')
    fields = ['tag']
    permission_required = 'crm_app.change_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update of :  ' + str(context['tag'])
        return context

    # def form_valid(self, form):
    #     edit_form = form.save(commit=False)
    #     edit_form.created_by = self.request.user
    #     self.object = form.save()
    #     return super().form_valid(form)

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Rendering form to delete tag
    """
    model = Tags
    template_name = 'crm_app/tag/tag_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('tag_list')
    permission_required = 'crm_app.delete_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete of:  ' + str(context['tag'])
        return context

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
