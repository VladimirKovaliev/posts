from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """Форма для модели поста"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
