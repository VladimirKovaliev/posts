from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, UpdateView, DeleteView


class PostListCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:home')
        return render(request, 'posts/create_post.html', {'form': form})


# class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [AllowAny]

class PostUpdateView(AllowAny, UpdateView):
    model = Post
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('posts:home')
    template_name = 'posts/create_post.html'


class PostDeleteView(AllowAny, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:home')


def custom_permission_denied_handler(request, exception):
    return Response({'detail': 'У вас нет прав для выполнения этого действия'}, status=401)


class HomeView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'post_list'


def contact(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'({phone}): {message}')

    context = {
        'title': 'Контакты'
    }

    return render(request, 'posts/contact.html', context)


class PostDetailView(AllowAny, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
