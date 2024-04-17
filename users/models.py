from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=20, verbose_name='Телефон', unique=True)
    email = models.EmailField(verbose_name='Email', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    subscribed = models.BooleanField(default=False, verbose_name='Подписка')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'Пользователь - {self.phone}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
