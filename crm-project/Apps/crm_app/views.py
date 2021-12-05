from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ClientsInfo
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
        form = ClientsInfoForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
        else:
            errors = 'some errors'
    form = ClientsInfoForm()
    return render(request,
                  'create_clients_info.html',
                  dict(form=form, errors=errors)
                  )
