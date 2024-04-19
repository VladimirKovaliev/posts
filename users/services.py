import stripe
from django.urls import reverse
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_session(request, plan_name, plan_price):
    """Создание сессии для оплаты подписки"""
    plan_price_cents = int(plan_price[:-1]) * 100 # -1 удаляет знак $, 100 переводит в центы

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan_name,
                },
                'unit_amount': plan_price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('users:success_subscription')),
        cancel_url=request.build_absolute_uri(reverse('users:cancel_subscription')),
    )

    return session
