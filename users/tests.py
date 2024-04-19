# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.contrib.messages import get_messages
#
# from users.models import User
#
#
# class UserViewsTestCase(TestCase):
#     def setUp(self):
#         self.register_url = reverse('users:register')
#         self.subscription_plans_url = reverse('users:subscription_plans')
#
#     def test_register_view(self):
#         response = self.client.get(self.register_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/register.html')
#
#         # Test registration form submission
#         response = self.client.post(self.register_url, {
#             'phone': '78005553535',
#             'password1': 'testpassword',
#             'password2': 'testpassword',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after successful registration
#         self.assertTrue(User.objects.filter(phone='78005553535').exists())  # Check if user was created
#
#     def test_subscription_plans_view(self):
#         response = self.client.get(self.subscription_plans_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/subscription_plans.html')
#
#         # Test subscription plan purchase
#         response = self.client.post(self.subscription_plans_url, {'plan_name': 'Basic'})
#         self.assertEqual(response.status_code, 302)
