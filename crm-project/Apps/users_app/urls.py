from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('user/', include([
        path('list/', views.UsersListView.as_view(), name='user_list'),
        path('detail/', views.UserDetailView.as_view(), name='user_detail'),
        path('update/', views.UserUpdateView.as_view(), name='user_update'),
        path('registration/', views.UserRegisterView.as_view(), name='registration'),
        path('change_password/', views.UserUpdatePasswordView.as_view(), name='change_password'),

        path(
            'reset_password/',
            auth_views.PasswordResetView.as_view(
                template_name='users_app/registration/reset_password.html'
            ),
            name='reset_password'
        ),
        path(
            'reset_password_sent/',
            auth_views.PasswordResetDoneView.as_view(
                template_name='users_app/registration/password_reset_sent.html'
            ),
            name='password_reset_done'
        ),
        path(
            'reset/<uidb64>/<token>',
            auth_views.PasswordResetConfirmView.as_view(
                template_name='users_app/registration/password_reset_form.html'
            ),
            name='password_reset_confirm'
        ),
        path(
            'reset_password_complete/',
            auth_views.PasswordResetCompleteView.as_view(
                template_name='users_app/registration/password_reset_done.html'
            ),
            name='password_reset_complete'
        ),
    ])),
]
