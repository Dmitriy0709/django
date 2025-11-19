# myauth/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class GetCookieViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_get_cookie_view(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(
            reverse("accounts:get_cookie"),
            HTTP_USER_AGENT="Mozilla/5.0 Test"
        )
        # Измени на реальный текст из шаблона
        self.assertContains(response, "Your Cookie Data")
