"""
Модели приложения shopapp (магазин товаров)
"""
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """
    Модель товара
    Представляет товар в магазине и связана с пользователем, который его создал
    Связь: много товаров на одного пользователя (ForeignKey)
    """
    # Название товара
    name = models.CharField(
        max_length=200,
        verbose_name='Название товара'
    )

    # Описание товара
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    # Цена товара
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )

    # Количество в наличии
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Количество в наличии'
    )

    # Изображение товара
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name='Изображение товара'
    )

    # Пользователь, создавший товар (КЛЮЧЕВОЕ ПОЛЕ)
    # Один пользователь может создавать много товаров
    # При удалении пользователя товар не удаляется (PROTECT)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_products',
        verbose_name='Создано пользователем'
    )

    # Дата создания товара
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    # Дата последнего обновления
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    # Активен ли товар
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        # Пользовательские разрешения
        permissions = [
            ('can_create_product', 'Может создавать товар'),
            ('can_edit_product', 'Может редактировать товар'),
            ('can_delete_product', 'Может удалять товар'),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Получить абсолютный URL товара"""
        from django.urls import reverse
        return reverse('product_detail', kwargs={'pk': self.pk})


class Category(models.Model):
    """
    Модель категории товара
    """
    # Название категории
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )

    # Описание категории
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    # Дата создания
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель заказа
    Представляет заказ от покупателя
    """
    # Возможные статусы заказа
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    # Пользователь, сделавший заказ
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель'
    )

    # Статус заказа
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    # Общая сумма заказа
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма заказа'
    )

    # Дата создания заказа
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    # Дата последнего обновления
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.pk} - {self.user.username}'


class OrderItem(models.Model):
    """
    Модель предмета в заказе
    Представляет отдельный товар в заказе
    """
    # Заказ, к которому относится товар
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )

    # Товар
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )

    # Количество товара в заказе
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    # Цена товара на момент заказа
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )

    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    @property
    def total_price(self):
        """Вычисление общей цены товара в заказе"""
        return self.quantity * self.price
