from django.urls import path, include
from .views import client_views, project_views, interplay_views, tag_views

urlpatterns = [

    path('client/', include([
        path('list_2/', client_views.ClientListView_2.as_view(), name='client_list_2'),
        # path('list/', client_views.ClientListView.as_view(), name='client_list'),
        path('add/', client_views.ClientAddView.as_view(), name='client_add'),
        path('<int:pk>/detail/', client_views.ClientDetailView.as_view(), name='client_detail'),
        path('<int:pk>/update/', client_views.ClientUpdateView.as_view(), name='client_update'),
        path('<int:pk>/delete/', client_views.ClientDeleteView.as_view(), name='client_delete'),
    ])),

    path('project/', include([
        path('list/', project_views.ProjectListView.as_view(), name='project_list'),
        path('add/', project_views.ProjectAddView.as_view(), name='project_add'),
        path('<int:pk>/detail/', project_views.ProjectDetailView.as_view(), name='project_detail'),
        path('<int:pk>/update/', project_views.ProjectUpdateView.as_view(), name='project_update'),
        path('<int:pk>/delete/', project_views.ProjectDeleteView.as_view(), name='project_delete'),
    ])),

    path('interplay/', include([
        path('list/', interplay_views.InterplayListView.as_view(), name='interplay_list'),
        path('add/', interplay_views.InterplayAddView.as_view(), name='interplay_add'),
        path('<int:pk>/detail/', interplay_views.InterplayDetailView.as_view(), name='interplay_detail'),
        path('<int:pk>/update/', interplay_views.InterplayUpdateView.as_view(), name='interplay_update'),
        path('<int:pk>/delete/', interplay_views.InterplayDeleteView.as_view(), name='interplay_delete'),
    ])),

    path('tag/', include([
        path('list/', tag_views.TagListView.as_view(), name='tag_list'),
        path('add/', tag_views.TagAddView.as_view(), name='tag_add'),
        path('<int:pk>/detail/', tag_views.TagDetailView.as_view(), name='tag_detail'),
        path('<int:pk>/update/', tag_views.TagUpdateView.as_view(), name='tag_update'),
        path('<int:pk>/delete/', tag_views.TagDeleteView.as_view(), name='tag_delete'),
    ])),
]
