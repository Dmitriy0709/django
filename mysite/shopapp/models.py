from django.db import models
from django.contrib.auth.models import User


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )

class Product(models.Model):
    """
    Модель продукта с связью на пользователя.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        help_text='Пользователь, который создал этот продукт'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']
        permissions = [
            ('can_create_product', 'Can create product'),
            ('can_edit_product', 'Can edit product'),
            ('can_delete_product', 'Can delete product'),
        ]

    def __str__(self):
        return self.name

    def can_edit(self, user):
        """
        Проверяет, может ли пользователь редактировать этот продукт.
        Разрешено только суперпользователю или автору с правами на редактирование.
        """
        if user.is_superuser:
            return True
        return user == self.created_by and user.has_perm('shopapp.can_edit_product')

    def can_delete(self, user):
        """
        Проверяет, может ли пользователь удалить этот продукт.
        """
        if user.is_superuser:
            return True
        return user == self.created_by and user.has_perm('shopapp.can_delete_product')


class Order(models.Model):
    """
    Модель заказа.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text='Пользователь, который создал заказ'
    )
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        help_text='Продукты в заказе'
    )
    delivery_address = models.TextField()
    promocode = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    receipt = models.FileField(null=True, upload_to='orders/receipts/')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
        # НЕ добавляем view_order - Django создает его автоматически

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def get_total_price(self):
        """
        Рассчитывает общую стоимость заказа.
        """
        return sum(product.price for product in self.products.all())
