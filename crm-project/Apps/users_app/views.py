from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from .forms import LoginUserForm, UserRegisterForm


# Create your views here.
Users = get_user_model()


class home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users_app/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    # def get_success_url(self):
    #     return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('/')


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Rendering list view for users
    """
    model = Users
    template_name = 'users_app/users_list.html'
    context_object_name = 'users'
    permission_required = 'users_app.view_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """
    Rendering profile Information
    """
    model = Users
    template_name = 'users_app/user_detail.html'
    context_object_name = 'user'
    permission_required = 'users_app.view_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile of: ' + str(context['user'])
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Rendering update for profile Information
    """
    model = Users
    template_name = 'users_app/user_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_detail')
    permission_required = 'users_app.change_users'
    fields = ['username', 'first_name', 'last_name', 'email', 'image',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit of: ' + str(context['user'])
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return self.request.user


class UserUpdatePasswordView(PasswordChangeView):
    """
    Rendering update password for profile Information
    """
    success_url = reverse_lazy('user_detail')
    template_name = 'users_app/user_password_update.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password for: ' + str(self.request.user)
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return self.request.user


class UserRegisterView(CreateView):
    """
    Rendering registered form
    """
    form_class = UserRegisterForm
    model = Users
    template_name = 'users_app/registration.html'
    success_url = reverse_lazy('user_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'registration'
        return context

