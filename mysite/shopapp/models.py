from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )

class Product(models.Model):
    """
    Модель Product представляет товар.
    который можно продавать в интернет магазине.

    Заказы тут:model:shopapp.Order
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        help_text=_('User who created this product')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
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


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    """
    Модель заказа.
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text=_('User who created the order')
    )
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        help_text=_('Products in the order')
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
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def get_total_price(self):
        """
        Рассчитывает общую стоимость заказа.
        """
        return sum(product.price for product in self.products.all())
