from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.usersHome, name='usersHome'),
    path('listUsers/', views.listUsers, name='listUsers'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),


    path('user/', include([
        path('list/', views.UsersListView.as_view(), name='user_list'),
        path('detail/', views.UserDetailView.as_view(), name='user_detail'),
        path('update/', views.UserUpdateView.as_view(), name='user_update'),
        path('change_password/', views.UserUpdatePasswordView.as_view(), name='change_password'),
        path('registration/', views.UserRegisterView.as_view(), name='registration'),

    ])),

]
