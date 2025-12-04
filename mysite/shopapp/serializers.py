"""
Сериализаторы для API приложения shopapp.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, ProductImage


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User (только для чтения).
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений продукта.
    """

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.
    """
    created_by = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'created_by',
            'created_at',
            'updated_at',
            'archived',
            'preview',
            'images',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def create(self, validated_data):
        """
        Создание продукта с автоматическим присвоением created_by.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    """
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Product.objects.all(),
        source='products'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'products',
            'product_ids',
            'delivery_address',
            'promocode',
            'status',
            'created_at',
            'updated_at',
            'receipt',
            'total_price',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_total_price(self, obj):
        """
        Вычисление общей стоимости заказа.
        """
        return obj.get_total_price()

    def create(self, validated_data):
        """
        Создание заказа с автоматическим присвоением user.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)
