from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.usersHome, name='usersHome'),
    path('listUsers/', views.listUsers, name='listUsers'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('user/', include([
        path('list/', views.UsersListView.as_view(), name='user_list'),
        path('<int:pk>/detail/', views.UserDetailView.as_view(), name='user_detail'),
        # path('detail/', views.UserDetailView.as_view(), name='user_detail'),
        # path('update/', views.UserUpdateView.as_view(), name='user_update'),
        path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),


        # path('add/', tag_views.TagAddView.as_view(), name='tag_add'),
        # path('<int:pk>/detail/', tag_views.TagDetailView.as_view(), name='tag_detail'),
        # path('<int:pk>/update/', tag_views.TagUpdateView.as_view(), name='tag_update'),
        # path('<int:pk>/delete/', tag_views.TagDeleteView.as_view(), name='tag_delete'),
    ])),


]
