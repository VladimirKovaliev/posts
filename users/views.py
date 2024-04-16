from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render

from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterForm
from users.models import User
from django.views import View
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import render, redirect
import stripe


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

    plans = [
        {'name': 'Basic', 'price': '10 $', 'description': 'Базовая подписка на 1 месяц', 'duration': '1 месяц'},
        {'name': 'Standard', 'price': '20 $', 'description': 'Стандартная подписка на 3 месяца',
         'duration': '3 месяца'},
        {'name': 'Premium', 'price': '30 $', 'description': 'Премиум подписка на 1 год', 'duration': '1 год'},
    ]
    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')

        plan_price = next((plan['price'] for plan in plans if plan['name'] == plan_name), 0)

        if plan_price == 0:
            return HttpResponseBadRequest('Invalid plan name')

        plan_price_cents = int(plan_price[:-1]) * 100

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan_name,
                    },
                    'unit_amount': plan_price_cents,  # Используем цену плана
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('users:success_subscription')),
            cancel_url=request.build_absolute_uri(reverse('users:cancel_subscription')),
        )

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
