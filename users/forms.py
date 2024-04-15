from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=20, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': '78005553535'}))

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2',)
