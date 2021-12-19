from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import ClientsInfo, ProjectsList, InterPlaysList, Tags
from .forms import ClientsPhonesFormSet, ClientsEmailsFormSet
from .filters import ClientsInfoFilter, InterplaysFilter


# Create your views here.

def crmHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --CRM-- </h1>')


headers = {
    'title': 'asc',
    'date_created': 'asc',
}


# ClientsList
class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
# class ClientListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = ClientsInfo
    template_name = 'client/clients_list.html'
    context_object_name = 'clients'
    paginate_by = 2
    permission_required = 'crm_app.view_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients List'
        sort = self.request.GET.get('sort')
        context['sort'] = sort
        return context

    def get_queryset(self):
        queryset = ClientsInfo.objects.all()
        sort = self.request.GET.get('sort')
        page = self.request.GET.get('page')
        if page is None:
            if sort is not None:
                if headers[sort] == "des":
                    queryset = ClientsInfo.objects.all().order_by(sort).reverse()
                    headers[sort] = "asc"
                else:
                    queryset = ClientsInfo.objects.all().order_by(sort)
                    headers[sort] = "des"
        elif sort is not None:
            if headers[sort] == "des":
                queryset = ClientsInfo.objects.all().order_by(sort)
            elif headers[sort] == "asc":
                queryset = ClientsInfo.objects.all().order_by(sort).reverse()
        return queryset.select_related('created_by')


class ClientListView_2(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClientsInfo
    filterset_class = ClientsInfoFilter
    template_name = 'client/clients_list_2.html'
    context_object_name = 'clients'
    paginate_by = 2
    permission_required = 'crm_app.view_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = ClientsInfo.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct().select_related('created_by')


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ClientsInfo
    template_name = 'client/client_detail.html'
    context_object_name = 'client'
    permission_required = 'crm_app.view_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Client: ' + str(context['client'])
        return context


class ClientAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClientsInfo
    template_name = 'client/client_add.html'
    success_url = reverse_lazy('home')
    fields = ['title', 'head', 'summary', 'address', ]
    permission_required = 'crm_app.add_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        if self.request.POST:
            context['inlinesPhones'] = ClientsPhonesFormSet(self.request.POST)
            context['inlinesEmails'] = ClientsEmailsFormSet(self.request.POST)
        else:
            context['inlinesPhones'] = ClientsPhonesFormSet()
            context['inlinesEmails'] = ClientsEmailsFormSet()
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        context = self.get_context_data()
        inlinesPhones = context['inlinesPhones']
        inlinesEmails = context['inlinesEmails']
        self.object = form.save()
        if inlinesPhones.is_valid():
            inlinesPhones.instance = self.object
            inlinesPhones.save()
        if inlinesEmails.is_valid():
            inlinesEmails.instance = self.object
            inlinesEmails.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ClientsInfo
    template_name = 'client/client_update.html'
    # fields = '__all__'
    fields = ['title', 'head', 'summary', 'address', ]
    permission_required = 'crm_app.change_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        if self.request.POST:
            context['inlinesPhones'] = ClientsPhonesFormSet(self.request.POST, instance=self.object)
            context['inlinesEmails'] = ClientsEmailsFormSet(self.request.POST, instance=self.object)
        else:
            context['inlinesPhones'] = ClientsPhonesFormSet(instance=self.object)
            context['inlinesEmails'] = ClientsEmailsFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        inlinesPhones = context['inlinesPhones']
        inlinesEmails = context['inlinesEmails']
        self.object = form.save()
        if inlinesPhones.is_valid():
            inlinesPhones.instance = self.object
            inlinesPhones.save()
        if inlinesEmails.is_valid():
            inlinesEmails.instance = self.object
            inlinesEmails.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ClientsInfo
    template_name = 'client/client_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_clientsinfo'


# ProjectsList
class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ProjectsList
    template_name = 'project/projects_list.html'
    context_object_name = 'projects'
    permission_required = 'crm_app.view_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects List'
        return context


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ProjectsList
    template_name = 'project/project_detail.html'
    context_object_name = 'project'
    permission_required = 'crm_app.view_projectlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project: ' + str(context['project'])
        return context


class ProjectAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ProjectsList
    template_name = 'project/project_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['client', 'p_name', 'description',
              'date_begin', 'date_end', 'value', ]
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


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ProjectsList
    template_name = 'project/project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_projectlist'


# InterplaysList
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


# Tags
class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Tags
    template_name = 'tag/tags_list.html'
    context_object_name = 'tags'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags List'
        return context


class TagDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Tags
    template_name = 'tag/tag_detail.html'
    context_object_name = 'tag'
    permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag: ' + str(context['tag'])
        return context


class TagAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tags
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


class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tags
    template_name = 'tag/tag_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('home')
    permission_required = 'crm_app.delete_tags'

#
# def CreateClientsInfoView(request):
#     errors = ''
#     if request.method == 'POST':
#         form = ClientsInfoForm(data=request.POST)
#         if form.is_valid:
#             edit_form = form.save(commit=False)
#             edit_form.created_by = request.user
#
#             edit_form.save()
#             form.save_m2m()
#
#             phone_1 = '+38099765400000'
#             phone_2 = '+380997654001'
#             phone_3 = '+380997654002'
#             list_phones = [phone_1, phone_2, phone_3]
#             for phone in list_phones:
#                 qs = ClientsPhones.objects.filter(phoneNumber=phone)
#                 if qs.exists():
#                     phonenumber = ClientsPhones.objects.get(phoneNumber=phone)
#                 else:
#                     phonenumber = ClientsPhones(phoneNumber=phone)
#                     phonenumber.save()
#                 edit_form.phoneNumber.add(phonenumber)
#             return redirect('home')
#         else:
#             errors = 'some errors'
#     form = ClientsInfoForm()
#     return render(request,
#                   'create_clients_info.html',
#                   dict(form=form, errors=errors)
#                   )
#
#     # new_form.title = 'petro'



