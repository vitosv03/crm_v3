from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ..models import ClientsInfo
from ..forms import ClientsPhonesFormSet, ClientsEmailsFormSet
from ..filters import ClientsInfoFilter
from ..utils import headers


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    # login_url = reverse_lazy('login')
    model = ClientsInfo
    template_name = 'client/clients_list.html'
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
    model = ClientsInfo
    # login_url = reverse_lazy('login')
    filterset_class = ClientsInfoFilter
    template_name = 'client/clients_list_2.html'
    context_object_name = 'clients'
    paginate_by = 4
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
    # login_url = reverse_lazy('login')
    template_name = 'client/client_detail.html'
    context_object_name = 'client'
    permission_required = 'crm_app.view_clientsinfo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Client: ' + str(context['client'])
        return context


class ClientAddView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClientsInfo
    # login_url = reverse_lazy('login')
    template_name = 'client/client_add.html'
    success_url = reverse_lazy('client_list_2')
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
    model = ClientsInfo
    # login_url = reverse_lazy('login')
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

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ClientsInfo
    # login_url = reverse_lazy('login')
    template_name = 'client/client_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('client_list_2')
    permission_required = 'crm_app.delete_clientsinfo'

    # проверка на автора записи
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)
