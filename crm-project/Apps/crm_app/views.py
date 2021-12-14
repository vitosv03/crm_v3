from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import ClientsInfo, ClientsPhones, ClientsEmails, ProjectsList, InterPlaysList, Tags
from .forms import ClientsInfoForm, ClientsPhonesFormSet, ClientsEmailsFormSet


# Create your views here.

def crmHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --CRM-- </h1>')


# ClientsList
class ClientsListView(ListView):
    model = ClientsInfo
    template_name = 'clients_list.html'
    context_object_name = 'clients'
    # ordering = ['title']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients List'
        return context

    def get_queryset(self):
        queryset = ClientsInfo.objects.all()
        if self.request.GET.get('s_sort'):
            selection = self.request.GET.get('s_sort')
            if selection == '-title':
                queryset = ClientsInfo.objects.order_by('-title')
            elif selection == 'title':
                queryset = ClientsInfo.objects.order_by('title')
        return queryset


class ClientsDetailView(DetailView):
    model = ClientsInfo
    template_name = 'client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Client: ' + str(context['client'])
        return context


class ClientsAddView(CreateView):
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
class ProjectsListView(ListView):
    model = ProjectsList
    template_name = 'projects_list.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects List'
        return context


class ProjectsDetailView(DetailView):
    model = ProjectsList
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Project: ' + str(context['project'])
        return context


class ProjectsAddView(CreateView):
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


class ProjectsUpdateView(UpdateView):
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


class ProjectsDeleteView(DeleteView):
    model = ProjectsList
    template_name = 'project_delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('home')


# InterplaysList
class InterplaysListView(ListView):
    model = InterPlaysList
    template_name = 'interplays_list.html'
    context_object_name = 'interplays'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplays List'
        return context


class InterplaysDetailView(DetailView):
    model = InterPlaysList
    template_name = 'interplay_detail.html'
    context_object_name = 'interplay'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Interplay: ' + str(context['interplay'])
        return context


class InterplaysAddView(CreateView):
    model = InterPlaysList
    template_name = 'interplay_add.html'
    success_url = reverse_lazy('home')
    # fields = '__all__'
    fields = ['project', 'link', 'description', 'rating', 'tag', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def form_valid(self, form):
        edit_form = form.save(commit=False)
        edit_form.created_by = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class InterplaysUpdateView(UpdateView):
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


class InterplaysDeleteView(DeleteView):
    model = InterPlaysList
    template_name = 'interplay_delete.html'
    context_object_name = 'interplay'
    success_url = reverse_lazy('home')


# Tags
class TagsListView(ListView):
    model = Tags
    template_name = 'tags_list.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tags List'
        return context



class TagAddView(CreateView):
    model = Tags
    template_name = 'tag_add.html'
    # success_url = reverse_lazy('home')
    fields = '__all__'
    # fields = ['project', 'link', 'description', 'rating', 'tag', ]

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

