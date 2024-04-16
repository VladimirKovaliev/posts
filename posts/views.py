from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.permissions import AllowAny
from django.contrib.auth.mixins import LoginRequiredMixin

from users.views import subscription_plans
from .forms import PostForm
from .models import Post
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


class PostListCreateView(View):
    """Отвечает за список и создание постов"""

    def get(self, request):
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:home')
        return render(request, 'posts/create_post.html', {'form': form})


class PostUpdateView(AllowAny, UpdateView):
    """Обрабатывает обновление существующих постов."""
    model = Post
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('posts:home')
    template_name = 'posts/create_post.html'


class PostDeleteView(AllowAny, DeleteView):
    """Обрабатывает удаление существующих постов."""
    model = Post
    success_url = reverse_lazy('posts:home')


class HomeView(ListView):
    """Отображает домашнюю страницу с списками постов на основе подписки пользователя."""
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.subscribed:
                """Пользователь с подпиской видит все посты"""
                return Post.objects.all()
            else:
                """Пользователь без подписки видит только посты пользователей без подписки"""
                return Post.objects.exclude(author__subscribed=True)
        else:
            """Неавторизированным отображаются только посты пользователей без подписки"""
            return Post.objects.exclude(author__subscribed=True)


def contact(request):
    """Обрабатывает отправку контактной формы."""
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        print(f'({name}): {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'posts/contact.html', context)


class PostDetailView(AllowAny, DetailView):
    """Выводит детали созданного пользователем поста"""
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class SubscriptionPostListCreateView(LoginRequiredMixin, View):
    """Обрабатывает создание поста для пользователей с подпиской"""

    def get(self, request):
        form = PostForm()
        return render(request, 'posts/subscription_create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() and request.user.subscribed:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:subscription_posts')
        return render(request, 'posts/subscription_create_post.html', {'form': form})


class SubscriptionPostListView(LoginRequiredMixin, View):
    """Отображает посты для пользователей с подпиской"""

    def get(self, request):
        if request.user.is_authenticated and request.user.subscribed:  # Проверяем подписку пользователя
            post_list = Post.objects.filter(author=request.user)
            return render(request, 'posts/subscription_posts.html', {'post_list': post_list})
        else:
            messages.info(request, 'Для начала необходимо приобрести подписку')
            return subscription_plans(request)
