from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Apps.crm_app.models import ClientsInfo, ClientsPhones, ClientsEmails
from Apps.crm_app.forms import ClientsPhonesFormSet, ClientsEmailsFormSet
from Apps.crm_app.filters import ClientsInfoFilter
from Apps.crm_app.utils import headers


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Rendering list of all clients
    """
    model = ClientsInfo
    template_name = 'crm_app/client/clients_list.html'
    context_object_name = 'clients'
    paginate_by = 4
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
    """
    Rendering list of all clients
    """
    model = ClientsInfo
    filterset_class = ClientsInfoFilter
    template_name = 'crm_app/client/clients_list_2.html'
    context_object_name = 'clients'
    paginate_by = 4
    permission_required = 'crm_app.view_clientsinfo'
    # queryset = ClientsInfo.objects.select_related('created_by',).all()
    # queryset = ClientsInfo.objects.defer('title',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients List_2'
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct().select_related('created_by',)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Rendering list detail info about of one client
    """
    model = ClientsInfo
    template_name = 'crm_app/client/client_detail.html'
    context_object_name = 'client'
    permission_required = 'crm_app.view_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail of: ' + str(context['client'])
        context['owner'] = self.object.created_by == self.request.user
        return context

    def get_queryset(self):
        return super().get_queryset().select_related('created_by')


class ClientAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Rendering form to add a new client
    """
    model = ClientsInfo
    template_name = 'crm_app/client/client_add.html'
    success_url = reverse_lazy('client_list_2')
    fields = ['title', 'head', 'summary', 'address', ]
    permission_required = 'crm_app.add_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new Client'
        if self.request.POST:
            context['inlinesPhones'] = ClientsPhonesFormSet(self.request.POST)
            context['inlinesEmails'] = ClientsEmailsFormSet(self.request.POST)
        else:
            context['inlinesPhones'] = ClientsPhonesFormSet()
            context['inlinesEmails'] = ClientsEmailsFormSet()
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        context = self.get_context_data()
        inlinesPhones = context['inlinesPhones']
        inlinesEmails = context['inlinesEmails']
        self.object = obj.save()
        self.object = form.save()
        if inlinesPhones.is_valid():
            inlinesPhones.instance = self.object
            inlinesPhones.save()
        if inlinesEmails.is_valid():
            inlinesEmails.instance = self.object
            inlinesEmails.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Rendering form to update a new client
    """
    model = ClientsInfo
    context_object_name = 'client'
    template_name = 'crm_app/client/client_update.html'
    fields = ['is_active', 'title', 'head', 'summary', 'address', ]
    permission_required = 'crm_app.change_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Client: ' + str(context['client'])
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

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Rendering form to delete client
    """
    model = ClientsInfo
    template_name = 'crm_app/client/client_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('client_list_2')
    permission_required = 'crm_app.delete_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete of: ' + str(context['client'])
        return context

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
