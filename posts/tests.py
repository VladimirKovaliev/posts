from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .views import PostListCreateView, HomeView, SubscriptionPostListCreateView, SubscriptionPostListView


class PostListCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_request(self):
        url = reverse('posts:create_post')
        request = self.factory.get(url)
        response = PostListCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_post_request(self):
        url = reverse('posts:create_post')
        data = {'title': 'Test Post', 'content': 'Test Content'}
        request = self.factory.post(url, data)
        response = PostListCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirects after successful POST


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)

    def test_authenticated_user_subscribed(self):
        url = reverse('posts:home')
        request = self.factory.get(url)
        request.user = self.user
        request.user.subscribed = True
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_authenticated_user_not_subscribed(self):
        url = reverse('posts:home')
        request = self.factory.get(url)
        request.user = self.user
        request.user.subscribed = False
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')

    def test_unauthenticated_user(self):
        url = reverse('posts:home')
        request = self.factory.get(url)
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')


class SubscriptionPostListCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_get_request(self):
        url = reverse('posts:subscription_create_post')
        request = self.factory.get(url)
        request.user = self.user
        response = SubscriptionPostListCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/subscription_create_post.html')

    def test_post_request_authenticated_user_subscribed(self):
        url = reverse('posts:subscription_create_post')
        data = {'title': 'Test Post', 'content': 'Test Content'}
        request = self.factory.post(url, data)
        request.user = self.user
        request.user.subscribed = True
        response = SubscriptionPostListCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirects after successful POST

    def test_post_request_authenticated_user_not_subscribed(self):
        url = reverse('posts:subscription_create_post')
        data = {'title': 'Test Post', 'content': 'Test Content'}
        request = self.factory.post(url, data)
        request.user = self.user
        request.user.subscribed = False
        response = SubscriptionPostListCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)  # Does not redirect if user is not subscribed


class SubscriptionPostListViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_authenticated_user_subscribed(self):
        url = reverse('posts:subscription_posts')
        request = self.factory.get(url)
        request.user = self.user
        request.user.subscribed = True
        response = SubscriptionPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/subscription_posts.html')

    def test_authenticated_user_not_subscribed(self):
        url = reverse('posts:subscription_posts')
        request = self.factory.get(url)
        request.user = self.user
        request.user.subscribed = False
        response = SubscriptionPostListView.as_view()(request)
        self.assertEqual(response.status_code, 200)  # Does not redirect if user is not subscribed

    def test_unauthenticated_user(self):
        url = reverse('posts:subscription_posts')
        request = self.factory.get(url)
        response = SubscriptionPostListView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirects unauthenticated users to subscription plans
