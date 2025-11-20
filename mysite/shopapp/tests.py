# shopapp/tests.py
from string import ascii_letters
from random import choices
from django.conf import settings
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
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

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
                "name": self.product_name,
                "price": "123.45",
                "description": "A good table",
                "discount": "10",
            }
        )
        self.assertRedirects(response, reverse("shopapp:product_list"))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создай пользователя для created_by
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Создай продукт со всеми обязательными полями
        cls.product = Product.objects.create(
            name="Best Product",
            price="99.99",
            description="Test product description",
            created_by=cls.user
        )

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()
        cls.user.delete()
        super().tearDownClass()

    def test_get_product(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Product")

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse("shopapp:product_detail", kwargs={"pk": self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):
    fixtures = ['products.json']

    def setUp(self):
        # Создай пользователя перед каждым тестом
        if not User.objects.filter(username='fixture_user').exists():
            User.objects.create_user(
                username='fixture_user',
                password='testpass123'
            )

    def test_products(self):
        response = self.client.get(reverse("shopapp:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fixture Product 1")
        self.assertContains(response, "Fixture Product 2")

class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='fixture_user', password='testpass123')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)

    def test_orders_view(self):
        response = self.client.get(reverse("shopapp:order_list"))
        self.assertContains(response, "Orders")

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("shopapp:order_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


