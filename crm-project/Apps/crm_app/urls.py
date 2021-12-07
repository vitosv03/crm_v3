from django.urls import path
from . import views

urlpatterns = [
    path('', views.crmHome, name='crmHome'),
    path('ClientsList/', views.ClientsListView, name='ClientsList'),
    path('CreateClientInfo/', views.CreateClientsInfoView, name='CreateClientInfo')
]
