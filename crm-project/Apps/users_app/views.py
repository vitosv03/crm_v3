from django.http import HttpResponse
from django.shortcuts import render


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
    # return HttpResponse('<h1>Home BASIC --USERS-- </h1>')
