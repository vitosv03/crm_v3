from django.urls import path
from . import views

urlpatterns = [
    path('', views.crmHome, name='crmHome'),
    path('ClientsInfo/', views.ClientsInfoView, name='ClientsInfo'),
    path('CreateClientInfo/', views.CreateClientsInfoView, name='CreateClientInfo')
]
