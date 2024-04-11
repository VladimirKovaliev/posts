from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterForm
from users.models import User
from django.views import View
from django.contrib.auth import logout



class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('posts:home')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        # Сохраняем пользователя, но пока не входим в систему
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect('users:verify_message')

    def get_success_url(self):
        return reverse('users:verify_message')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = RegisterForm
    success_url = 'users:users_list'

    def get_success_url(self):
        return reverse('users:list_view')
