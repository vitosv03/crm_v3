from django.http import HttpResponse
from django.shortcuts import render
from .models import Users

# Create your views here.

def usersHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --USERS-- </h1>')


def home(request):
    current_user = request.user
    return render(request,
                  'base.html',
                  dict(user=current_user)
                  )


def listUsers(request):
    all_users = Users.objects
    return render(request,
                  'list_users.html',
                  dict(all_users=all_users)
                  )
