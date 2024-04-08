from django.db import models

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    image = models.ImageField(upload_to='posts/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'