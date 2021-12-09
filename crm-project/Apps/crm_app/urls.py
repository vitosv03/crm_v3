from django.urls import path
from . import views

urlpatterns = [
    path('', views.crmHome, name='crmHome'),
    # path('ClientsList/', views.ClientsListView, name='ClientsList'),
    path('ClientsList/', views.ClientsListView.as_view(), name='ClientsList'),
    path('client/<int:pk>/', views.ClientsDetailView.as_view(), name='ClientDetail'),
    path('CreateClientInfo/', views.CreateClientsInfoView, name='CreateClientInfo')
]
