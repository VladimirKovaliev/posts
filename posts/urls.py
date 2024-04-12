from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, HomeView, contact
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
    path('contact/', contact, name='contact'),
]

