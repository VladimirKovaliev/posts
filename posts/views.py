from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.views.generic import ListView


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


def custom_permission_denied_handler(request, exception):
    return Response({'detail': 'У вас нет прав для выполнения этого действия'}, status=401)


class HomeView(ListView):
    model = Post
    template_name = 'posts/home.html'
