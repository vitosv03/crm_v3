from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def crmHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --CRM-- </h1>')
