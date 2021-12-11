from urllib import request

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import ClientsInfo, ClientsPhones, ClientsEmails
from .forms import ClientsInfoForm, ClientsPhonesFormSet, ClientsEmailsFormSet
from django.forms import inlineformset_factory


# Create your views here.

def crmHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --CRM-- </h1>')


class ClientsListView(ListView):
    model = ClientsInfo
    template_name = 'clients_list.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clients List'
        return context


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
    fields = '__all__'

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


# class ClientsAddView(CreateView):
#     model = ClientsInfo
#     form_class = ClientsInfoForm
#     template_name = 'client_add.html'
#     success_url = reverse_lazy('home')
#     fields = '__all__'
#
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.form_class
#         form = self.get_form(form_class)
#         clientsPhones_form = ClientsPhonesFormSet(self,request.POST)
#         clientsEmails_form = ClientsEmailsFormSet(self,request.POST)
#         if form.is_valid() and clientsPhones_form.is_valid() and clientsEmails_form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         clientsPhones_form = ClientsPhonesFormSet(self, request.POST)
#         clientsEmails_form = ClientsEmailsFormSet(self, request.POST)
#         self.object = form.save()
#         clientsPhones_form.instance = self.object
#         clientsPhones_form.save()
#         clientsEmails_form.instance = self.object
#         clientsEmails_form.save()
#         return HttpResponseRedirect (self.get_success_url())
#
#      # def form_invalid(self, form, clientsPhones_form, clientsEmails_form):
#      #    return self.render_to_response(
#      #        self.get_context_data(form=form,
#      #                              clientsPhones_form=clientsPhones_form,
#      #                              clientsEmails_form=clientsEmails_form))
#
#
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'title of page'
#         return context


# ClientsPhonesFormSet = inlineformset_factory(ClientsInfo, ClientsPhones, fields=('phoneNumber',))
# client = ClientsInfo.objects.get(id=1)
# formsetPhones = ClientsPhonesFormSet(instance=client)


# BookFormSet = inlineformset_factory(Author, Book, fields=('title',))
# author = Author.objects.get(name='Mike Royko')
# formset = BookFormSet(instance=author)


# def ClientsListView(request):
#     all_clients = ClientsInfo.objects.all()
#     return render(request,
#                   'clients_list.html',
#                   dict(all_users=all_clients)
#                   )

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
