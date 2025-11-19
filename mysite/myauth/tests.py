from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("accounts:get_cookie"))
        self.assertContains(response, "Cookie value")

