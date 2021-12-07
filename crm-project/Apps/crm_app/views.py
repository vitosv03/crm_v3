from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ClientsInfo, ClientsPhones
from .forms import ClientsInfoForm

# Create your views here.

def crmHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --CRM-- </h1>')


def ClientsInfoView(request):
    all_clients = ClientsInfo.objects.all()
    return render(request,
                  'clients_info.html',
                  dict(all_users=all_clients)
                  )


def CreateClientsInfoView(request):
    errors = ''
    if request.method == 'POST':
        form = ClientsInfoForm(data=request.POST)
        if form.is_valid:
            edit_form = form.save(commit=False)
            edit_form.created_by = request.user

            edit_form.save()
            form.save_m2m()

            phone_1 = '+380997654000'
            phone_2 = '+380997654001'
            phone_3 = '+380997654002'
            list_phones = [phone_1, phone_2, phone_3]
            for phone in list_phones:
                qs = ClientsPhones.objects.filter(phoneNumber=phone)
                if qs.exists():
                    phonenumber = ClientsPhones.objects.get(phoneNumber=phone)
                else:
                    phonenumber = ClientsPhones(phoneNumber=phone)
                    phonenumber.save()
                edit_form.phoneNumber.add(phonenumber)
            return redirect('home')
        else:
            errors = 'some errors'
    form = ClientsInfoForm()
    return render(request,
                  'create_clients_info.html',
                  dict(form=form, errors=errors)
                  )


            # new_form.title = 'petro'

