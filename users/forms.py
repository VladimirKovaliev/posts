from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User
from django.core.exceptions import ValidationError
import re


class PhoneValidator:
    def __call__(self, value):
        if not re.match(r'^\d{10,13}$', value):
            raise ValidationError('Номер телефона должен содержать от 10 до 13 цифр.')


class RegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    phone = forms.CharField(max_length=20, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '78005553535'}),
                            validators=[PhoneValidator()])

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2',)
