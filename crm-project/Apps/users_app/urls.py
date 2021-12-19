from django.urls import path
from . import views

urlpatterns = [
    path('', views.usersHome, name='usersHome'),
    path('listUsers/', views.listUsers, name='listUsers'),
    path('login/', views.LoginUserView.as_view(), name='login'),
]
