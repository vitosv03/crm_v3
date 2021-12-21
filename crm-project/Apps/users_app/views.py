from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Users
from django.contrib.auth.views import LoginView
from .forms import LoginUserForm
# Create your views here.

def usersHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --USERS-- </h1>')


def home(request):
    current_user = request.user
    return render(request, 'home.html', dict(user=current_user) )


def listUsers(request):
    all_users = Users.objects.all()
    return render(request,'list_users.html', dict(all_users=all_users))


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


# class TagListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
class UsersListView(LoginRequiredMixin, ListView):
    model = Users
    template_name = 'users_list.html'
    context_object_name = 'users'
    # permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context


# class TagDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
class UserDetailView(LoginRequiredMixin, DetailView):
    model = Users
    template_name = 'user_detail.html'
    context_object_name = 'user'
    # permission_required = 'crm_app.view_tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User: ' + str(context['user'])
        return context
