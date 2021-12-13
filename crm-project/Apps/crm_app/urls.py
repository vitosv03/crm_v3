from django.urls import path
from . import views

urlpatterns = [
    path('', views.crmHome, name='crmHome'),

    path('ClientsList/', views.ClientsListView.as_view(), name='ClientsList'),
    path('client/<int:pk>/', views.ClientsDetailView.as_view(), name='ClientDetail'),
    path('clientAdd/', views.ClientsAddView.as_view(), name='ClientAdd'),
    path('clientUpdate/<int:pk>/', views.ClientUpdateView.as_view(), name='clientUpdate'),
    path('clientDelete/<int:pk>/', views.ClientDeleteView.as_view(), name='clientDelete'),

    path('ProjectsList/', views.ProjectsListView.as_view(), name='ProjectsList'),
    path('project/<int:pk>/', views.ProjectsDetailView.as_view(), name='ProjectDetail'),
    path('projectAdd/', views.ProjectsAddView.as_view(), name='projectAdd'),
    path('projectUpdate/<int:pk>/', views.ProjectsUpdateView.as_view(), name='projectUpdate'),
    path('projectDelete/<int:pk>/', views.ProjectsDeleteView.as_view(), name='projectDelete'),

    path('InterplaysList/', views.InterplaysListView.as_view(), name='InterplaysList'),
    path('interplay/<int:pk>/', views.InterplaysDetailView.as_view(), name='InterplayDetail'),
    path('interplayAdd/', views.InterplaysAddView.as_view(), name='interplayAdd'),

]
