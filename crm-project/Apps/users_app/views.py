from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from .models import Users
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginUserForm


# Create your views here.

def usersHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --USERS-- </h1>')


def home(request):
    current_user = request.user
    return render(request, 'home.html', dict(user=current_user))


def listUsers(request):
    all_users = Users.objects.all()
    return render(request, 'list_users.html', dict(all_users=all_users))


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Users
    template_name = 'users_list.html'
    context_object_name = 'users'
    permission_required = 'users_app.view_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Users
    template_name = 'user_detail.html'
    context_object_name = 'user'
    permission_required = 'users_app.view_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User: ' + str(context['user'])
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Users
    template_name = 'user_update.html'
    success_url = reverse_lazy('user_detail')
    permission_required = 'users_app.change_users'
    fields = ['username', 'first_name', 'last_name', 'email', 'image',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)


class UserUpdatePasswordView(PasswordChangeView):
    success_url = reverse_lazy('user_detail')
    template_name = 'user_password_update.html'

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)
