from django.http import HttpResponse
from django.shortcuts import render
from .models import ClientsInfo

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
