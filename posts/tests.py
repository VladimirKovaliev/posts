from django.test import TestCase
from django.urls import reverse

from .models import Post
from users.models import User


class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone="123456789", password="testpassword")
        self.post = Post.objects.create(title="Test Post", content="This is a test post", author=self.user)

        def test_post_creation(self):
            post = Post.objects.create(title="Another Test Post", content="Another test post", author=self.user)
            self.assertEqual(post.title, "Another Test Post")
            self.assertEqual(post.content, "Another test post")
            self.assertEqual(post.author, self.user)