from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.crmHome, name='crmHome'),

    path('client/', include([
        path('list_2/', views.ClientListView_2.as_view(), name='client_list_2'),
        path('list/', views.ClientListView.as_view(), name='client_list'),
        path('add/', views.ClientAddView.as_view(), name='client_add'),
        path('<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
        path('<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
        path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    ])),

    path('project/', include([
        path('list/', views.ProjectListView.as_view(), name='project_list'),
        path('add/', views.ProjectAddView.as_view(), name='project_add'),
        path('<int:pk>/detail/', views.ProjectDetailView.as_view(), name='project_detail'),
        path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
        path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    ])),

    path('interplay/', include([
        path('list/', views.InterplayListView.as_view(), name='interplay_list'),
        path('add/', views.InterplayAddView.as_view(), name='interplay_add'),
        path('<int:pk>/detail/', views.InterplayDetailView.as_view(), name='interplay_detail'),
        path('<int:pk>/update/', views.InterplayUpdateView.as_view(), name='interplay_update'),
        path('<int:pk>/delete/', views.InterplayDeleteView.as_view(), name='interplay_delete'),
    ])),

    path('tag/', include([
        path('list/', views.TagListView.as_view(), name='tag_list'),
        path('add/', views.TagAddView.as_view(), name='tag_add'),
        path('<int:pk>/detail/', views.TagDetailView.as_view(), name='tag_detail'),
        path('<int:pk>/update/', views.TagUpdateView.as_view(), name='tag_update'),
        path('<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    ])),
]

