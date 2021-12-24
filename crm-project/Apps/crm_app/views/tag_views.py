from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import Tags


class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tags
    # login_url = reverse_lazy('login')
    template_name = 'tag/tags_list.html'
    context_object_name = 'tags'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags List'
        return context


class TagDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Tags
    # login_url = reverse_lazy('login')
    template_name = 'tag/tag_detail.html'
    context_object_name = 'tag'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag: ' + str(context['tag'])
        return context


class TagAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tags
    # login_url = reverse_lazy('login')
    template_name = 'tag/tag_add.html'
    success_url = reverse_lazy('home')
    fields = ['tag']
    permission_required = 'crm_app.add_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context


class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Tags
    # login_url = reverse_lazy('login')
    template_name = 'tag/tag_add.html'
    success_url = reverse_lazy('home')
    fields = '__all__'
    permission_required = 'crm_app.change_tags'

    # fields = ['project', 'link', 'description', 'rating', 'tag', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
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
    model = Tags
    # login_url = reverse_lazy('login')
    template_name = 'tag/tag_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_tags'

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
