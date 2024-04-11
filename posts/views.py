from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post
from .serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CustomPermissionDeniedHandler:
    def __init__(self, exc):
        self.exc = exc

    def __call__(self, *args, **kwargs):
        return Response({'detail': 'У вас нет прав для выполнения этого действия'}, status=401)
