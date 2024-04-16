from django.urls import path
from django.views.generic import TemplateView

from users import views
from users.apps import UsersConfig
from users.views import UserLogoutView, UserLoginView, RegisterView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('verify_message/', TemplateView.as_view(template_name='users/verify_message.html'), name='verify_message'),
    path('success_verify/', TemplateView.as_view(template_name='users/success_verify.html'), name='success_verify'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('edit/<int:pk>', UserUpdateView.as_view(), name='edit'),

    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('success/', views.success_subscription, name='success_subscription'),

]