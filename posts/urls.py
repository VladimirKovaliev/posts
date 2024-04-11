from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, HomeView
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
]

