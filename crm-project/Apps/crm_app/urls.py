from django.urls import path, include
from . import views

# urlpatterns = [
#     path('', views.crmHome, name='crmHome'),
#
#     path('ClientsList/', views.ClientsListView.as_view(), name='ClientsList'),
#     path('client/<int:pk>/', views.ClientsDetailView.as_view(), name='ClientDetail'),
#     path('clientAdd/', views.ClientsAddView.as_view(), name='ClientAdd'),
#     path('clientUpdate/<int:pk>/', views.ClientUpdateView.as_view(), name='clientUpdate'),
#     path('clientDelete/<int:pk>/', views.ClientDeleteView.as_view(), name='clientDelete'),
#
#     path('ProjectsList/', views.ProjectsListView.as_view(), name='ProjectsList'),
#     path('project/<int:pk>/', views.ProjectsDetailView.as_view(), name='ProjectDetail'),
#     path('projectAdd/', views.ProjectsAddView.as_view(), name='projectAdd'),
#     path('projectUpdate/<int:pk>/', views.ProjectsUpdateView.as_view(), name='projectUpdate'),
#     path('projectDelete/<int:pk>/', views.ProjectsDeleteView.as_view(), name='projectDelete'),
#
#     path('InterplaysList/', views.InterplaysListView.as_view(), name='InterplaysList'),
#     path('interplay/<int:pk>/', views.InterplaysDetailView.as_view(), name='InterplayDetail'),
#     path('interplayAdd/', views.InterplaysAddView.as_view(), name='interplayAdd'),
#     path('interplayUpdate/<int:pk>/', views.InterplaysUpdateView.as_view(), name='interplayUpdate'),
#     path('interplayDelete/<int:pk>/', views.InterplaysDeleteView.as_view(), name='interplayDelete'),
#
#     path('TagsList/', views.TagsListView.as_view(), name='TagsList'),
#     path('tag/<int:pk>/', views.TagsDetailView.as_view(), name='TagDetail'),
#     path('tagAdd/', views.TagAddView.as_view(), name='tagAdd'),
#     path('tagUpdate/<int:pk>/', views.TagUpdateView.as_view(), name='tagUpdate'),
#     path('tagDelete/<int:pk>/', views.TagsDeleteView.as_view(), name='tagDelete'),
#
# ]


urlpatterns = [
    path('', views.crmHome, name='crmHome'),

    path('client/', include([
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

