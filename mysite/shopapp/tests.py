# shopapp/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product
from .utils import add_two_numbers


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        # Создай пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Дай ему permission на создание продуктов
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.get(
            codename='can_create_product',
            content_type=content_type,
        )
        self.user.user_permissions.add(permission)

        # Залогинь пользователя
        self.client.login(username='testuser', password='testpass123')

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": "Table123",
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))

        # Дополнительно проверь что продукт создан
        self.assertTrue(
            Product.objects.filter(name="Table123").exists()
        )
