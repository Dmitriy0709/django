from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    """Product model with user relationship"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_create_product', 'Can create product'),
            ('can_edit_product', 'Can edit product'),
            ('can_delete_product', 'Can delete product'),
        ]

    def __str__(self):
        return self.name

    def can_edit(self, user):
        """Check if user can edit this product"""
        if user.is_superuser:
            return True
        if user.has_perm('shop.can_edit_product') and user == self.created_by:
            return True
        return False

    def can_delete(self, user):
        """Check if user can delete this product"""
        if user.is_superuser:
            return True
        if user.has_perm('shop.can_delete_product') and user == self.created_by:
            return True
        return False
