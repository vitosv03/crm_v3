

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .models import ClientsInfo, ClientsPhones
# from .forms import ClientsInfoForm


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
        return context




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
