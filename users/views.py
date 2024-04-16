from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
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


# def subscription_plans(request):
#     plans = [
#         {'name': 'Basic', 'price': '$10', 'description': 'Базовая подписка на 1 месяц', 'duration': '1 месяц'},
#         {'name': 'Standard', 'price': '$20', 'description': 'Стандартная подписка на 3 месяца', 'duration': '3 месяца'},
#         {'name': 'Premium', 'price': '$50', 'description': 'Премиум подписка на 1 год', 'duration': '1 год'},
#     ]
#     return render(request, 'users/subscription_plans.html', {'plans': plans})


stripe.api_key = settings.STRIPE_SECRET_KEY


def subscription_plans(request):
    if request.method == 'POST':
        # Получаем данные о выбранном плане подписки
        plan_name = request.POST.get('plan_name')

        # Создаем платеж через Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': plan_name,
                    },
                    'unit_amount': 1000,  # Цена плана в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/users/success/'),
            cancel_url=request.build_absolute_uri('/users/subscription_plans/'),
        )

        # Перенаправляем пользователя на страницу оплаты Stripe
        return redirect(session.url)

    # Если запрос GET, просто отображаем страницу с планами подписок
    plans = [
        {'name': 'Basic', 'price': '$10', 'description': 'Базовая подписка на 1 месяц', 'duration': '1 месяц'},
        {'name': 'Standard', 'price': '$20', 'description': 'Стандартная подписка на 3 месяца', 'duration': '3 месяца'},
        {'name': 'Premium', 'price': '$50', 'description': 'Премиум подписка на 1 год', 'duration': '1 год'},
    ]
    return render(request, 'users/subscription_plans.html', {'plans': plans})
