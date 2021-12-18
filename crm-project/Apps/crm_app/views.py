from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import ClientsInfo, ClientsPhones, ClientsEmails, ProjectsList, InterPlaysList, Tags
from .forms import ClientsInfoForm, ClientsPhonesFormSet, ClientsEmailsFormSet
# from .filters import ClientsInfoFilter, FilteredListView, ClientFilterSet
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
class ClientListView(ListView):
    model = ClientsInfo
    template_name = 'clients_list.html'
    context_object_name = 'clients'
    # ordering = ['title']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients List'
        sort = self.request.GET.get('sort')
        context['sort'] = sort
        return context

    # def get_queryset(self):
    #     queryset = ClientsInfo.objects.all()
    #     if self.request.GET.get('sort'):
    #         selection = self.request.GET.get('sort')
    #         if selection == 'asc':
    #             queryset = ClientsInfo.objects.order_by('title')
    #         elif selection == 'desc':
    #             queryset = ClientsInfo.objects.order_by('-title')
    #     return queryset

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
        return queryset


class ClientListView_2(ListView):
    model = ClientsInfo
    filterset_class = ClientsInfoFilter
    template_name = 'clients_list_2.html'
    context_object_name = 'clients'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = ClientsInfo.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()


class ClientDetailView(DetailView):
    model = ClientsInfo
    template_name = 'client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Client: ' + str(context['client'])
        return context


class ClientAddView(CreateView):
    model = ClientsInfo
    template_name = 'client_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['title', 'head', 'summary', 'address', ]

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


class ClientUpdateView(UpdateView):
    model = ClientsInfo
    template_name = 'client_update.html'
    # fields = '__all__'
    fields = ['title', 'head', 'summary', 'address', ]

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


class ClientDeleteView(DeleteView):
    model = ClientsInfo
    template_name = 'client_delete.html'
    context_object_name = 'client'
    success_url = reverse_lazy('home')


# ProjectsList
class ProjectListView(ListView):
    model = ProjectsList
    template_name = 'projects_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects List'
        return context



class ProjectDetailView(DetailView):
    model = ProjectsList
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project: ' + str(context['project'])
        return context


class ProjectAddView(CreateView):
    model = ProjectsList
    template_name = 'project_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['client', 'p_name', 'description',
              'date_begin', 'date_end', 'value', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    model = ProjectsList
    template_name = 'project_update.html'
    # success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['client', 'p_name', 'description',
              'date_begin', 'date_end', 'value', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = ProjectsList
    template_name = 'project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('home')


# InterplaysList
class InterplayListView(ListView):
    model = InterPlaysList
    template_name = 'interplays_list.html'
    context_object_name = 'interplays'
    filterset_class = InterplaysFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplays List'
        context['filter'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()



class InterplayDetailView(DetailView):
    model = InterPlaysList
    template_name = 'interplay_detail.html'
    context_object_name = 'interplay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplay: ' + str(context['interplay'])
        return context


class InterplayAddView(CreateView):
    model = InterPlaysList
    template_name = 'interplay_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['project', 'link', 'description', 'rating', 'tag', ]

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
        form.instance.description = 'sdfsdf'
        self.object = form.save()
        return super().form_valid(form)


class InterplayUpdateView(UpdateView):
    model = InterPlaysList
    template_name = 'interplay_update.html'
    # success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['link', 'description', 'rating', 'tag', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class InterplayDeleteView(DeleteView):
    model = InterPlaysList
    template_name = 'interplay_delete.html'
    context_object_name = 'interplay'
    success_url = reverse_lazy('home')


# Tags
class TagListView(ListView):
    model = Tags
    template_name = 'tags_list.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags List'
        return context


class TagDetailView(DetailView):
    model = Tags
    template_name = 'tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tag: ' + str(context['tag'])
        return context


class TagAddView(CreateView):
    model = Tags
    template_name = 'tag_add.html'
    success_url = reverse_lazy('home')
    fields = ['tag']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context


class TagUpdateView(UpdateView):
    model = Tags
    template_name = 'tag_add.html'
    success_url = reverse_lazy('home')
    fields = '__all__'

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


class TagDeleteView(DeleteView):
    model = Tags
    template_name = 'tag_delete.html'
    context_object_name = 'tag'
    success_url = reverse_lazy('home')

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
