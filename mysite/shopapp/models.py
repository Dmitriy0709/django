from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
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
