from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.views import View
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, redirect

from users.forms import RegisterForm
from users.models import User

from config.constants import PLANS

import stripe

from users.services import create_payment_session


class UserLoginView(LoginView):
    """Обработка входа пользователя"""
    template_name = 'users/login.html'


class UserLogoutView(View):
    """Обработка выхода пользователя"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('posts:home')


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Валидная форма регистрации пользователя"""
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect('users:verify_message')

    def get_success_url(self):
        """Получение URL для перенаправления после успешной регистрации"""
        return reverse('users:verify_message')


class UserUpdateView(PermissionRequiredMixin, UpdateView):
    """Обновление информации о пользователе"""
    model = User
    form_class = RegisterForm
    success_url = 'users:users_list'

    def get_success_url(self):
        """Получение URL для перенаправления после успешного обновления"""
        return reverse('users:list_view')


def subscription_plans(request):
    """Обработка тарифного плана для подписок"""
    stripe.api_key = settings.STRIPE_SECRET_KEY

    plans = PLANS
    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')

        plan_price = next((plan['price'] for plan in plans if plan['name'] == plan_name), 0)

        if plan_price == 0:
            return HttpResponseBadRequest('Что-то пошло не так. Пожалуйста, повторите попытку.')

        session = create_payment_session(request, plan_name, plan_price)

        return redirect(session.url)

    return render(request, 'users/subscription_plans.html', {'plans': plans})


def cancel_subscription(request):
    """URL для перенаправления в случае отмены платежа"""
    return render(request, 'users/cancel_payment.html')


def success_subscription(request):
    """Обработка оплаты подписки"""
    if request.user.is_authenticated:
        user = request.user
        if not user.subscribed:
            user.subscribed = True
            user.save()
            messages.success(request, 'Подписка успешно оформлена!')
        else:
            messages.info(request, 'У вас уже есть активная подписка.')
        return redirect('posts:home')
    else:
        messages.error(request, 'Что-то пошло не так. Пожалуйста, повторите попытку.')
        return redirect('users:login')
