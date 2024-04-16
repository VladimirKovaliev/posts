from django.urls import path
from .views import HomeView, contact, PostListCreateView, PostDetailView, \
    PostUpdateView, PostDeleteView, SubscriptionPostListCreateView, SubscriptionPostListView
from posts.apps import PostsConfig

app_name = PostsConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('contact/', contact, name='contact'),
    path('create/', SubscriptionPostListCreateView.as_view(), name='subscription_create_post'),
    path('subscription_posts/', SubscriptionPostListView.as_view(), name='subscription_posts'),
]