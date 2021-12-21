from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView

from .models import Users
from django.contrib.auth.views import LoginView
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

    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)


# class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    template_name = 'user_update.html'
    # success_url = reverse_lazy('home')
    # fields = '__all__'
    # permission_required = 'users_app.change_user'
    fields = ['username', 'first_name', 'last_name', 'email', 'image', ]



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'title of page'
        return context

    def get_object(self):
        return get_object_or_404(Users, pk=self.request.user.pk)
    # def form_valid(self, form):
    #     if self.request.method == 'POST':
    #         form = self.request.POST, self.request.FILES
    #     if form.is_valid():
    #         form.save()
    #     return super().form_valid(form)
