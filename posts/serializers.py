from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели поста"""
    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'avatar']
