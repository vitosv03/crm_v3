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


# надо удалить больше не используется
def usersHome(request):
    current_user = request.user
    return HttpResponse('<h1>Home --USERS-- </h1>')


class home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    # login_url = reverse_lazy('login')


# надо удалить больше не используется
def listUsers(request):
    # Users = get_user_model()
    all_users = Users.objects.all()
    return render(request, 'users_app/list_users.html', dict(all_users=all_users))


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users_app/login.html'

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
    # Users = get_user_model()
    model = Users
    # login_url = reverse_lazy('login')
    template_name = 'users_app/users_list.html'
    context_object_name = 'users'
    permission_required = 'users_app.view_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User List'
        return context


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # Users = get_user_model()
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
        # return get_object_or_404(Users, pk=self.request.user.pk)
        return self.request.user


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    # Users = get_user_model()
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
        # return get_object_or_404(Users, pk=self.request.user.pk)
        return self.request.user


class UserUpdatePasswordView(PasswordChangeView):
    success_url = reverse_lazy('user_detail')
    template_name = 'users_app/user_password_update.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Change Password for: ' + str(self.request.user)
        return context

    # за счет этой штуки можно открыть страницу без ИД
    def get_object(self):
        # return get_object_or_404(Users, pk=self.request.user.pk)
        return self.request.user


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    # User = get_user_model()
    model = Users
    template_name = 'users_app/registration.html'
    success_url = reverse_lazy('user_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'registration'
        return context

