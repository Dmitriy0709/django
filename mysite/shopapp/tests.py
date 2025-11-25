from string import ascii_letters
from random import choices
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Product, Order
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

    def test_products(self):
        response = self.client.get(reverse("shopapp:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fixture Product 1")
        self.assertContains(response, "Fixture Product 2")


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.credentials = dict(username='orders_test_user', password='testpass123')
        cls.user = User.objects.create_user(**cls.credentials)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

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


class ProductExportTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse("shopapp:products-export"),
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": product.pk,
                "name": product.name,
                "price": str(product.price),
                "archived": product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data["products"],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):
    """
    Тест для OrderDetailView.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = User.objects.create_user(
            username='order_detail_user',
            password='testpass123'
        )
        # Добавляем разрешение на просмотр заказа
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.get(
            codename='view_order',
            content_type=content_type,
        )
        cls.user.user_permissions.add(permission)

        # Создаем пользователя для продуктов
        cls.product_creator = User.objects.create_user(
            username='product_creator',
            password='testpass123'
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.product_creator.delete()
        super().tearDownClass()

    def setUp(self):
        # Вход пользователя
        self.client.login(username='order_detail_user', password='testpass123')

        # Создаем продукты для заказа
        self.product1 = Product.objects.create(
            name="Test Product 1",
            description="Description 1",
            price="100.00",
            created_by=self.product_creator
        )
        self.product2 = Product.objects.create(
            name="Test Product 2",
            description="Description 2",
            price="200.00",
            created_by=self.product_creator
        )

        # Создаем заказ
        self.order = Order.objects.create(
            user=self.user,
            delivery_address="123 Test Street, Test City",
            promocode="TESTCODE2024"
        )
        self.order.products.add(self.product1, self.product2)

    def tearDown(self):
        # Удаляем заказ и продукты после теста
        self.order.delete()
        self.product1.delete()
        self.product2.delete()

    def test_order_details(self):
        """
        Проверка получения деталей заказа.
        """
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order.pk})
        )

        # Проверяем статус ответа
        self.assertEqual(response.status_code, 200)

        # Проверяем, что в теле ответа есть адрес заказа
        self.assertContains(response, self.order.delivery_address)

        # Проверяем, что в теле ответа есть промокод
        self.assertContains(response, self.order.promocode)

        # Проверяем, что в контексте тот же заказ (по первичному ключу)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    """
    Тест для OrdersExportView.
    """
    fixtures = [
        'orders-export-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя с is_staff=True
        cls.user = User.objects.create_user(
            username='staff_user',
            password='testpass123',
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        # Вход пользователя
        self.client.login(username='staff_user', password='testpass123')

    def test_get_orders_export(self):
        """
        Проверка экспорта заказов.
        """
        response = self.client.get(reverse("shopapp:orders-export"))

        # Проверяем статус кода
        self.assertEqual(response.status_code, 200)

        # Получаем данные из ответа
        orders_data = response.json()

        # Проверяем структуру ответа
        self.assertIn('orders', orders_data)

        # Получаем все заказы из базы данных
        orders = Order.objects.select_related('user').prefetch_related('products').order_by('pk')

        # Формируем ожидаемые данные
        expected_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.pk,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        # Проверяем, что данные совпадают
        self.assertEqual(orders_data['orders'], expected_data)
