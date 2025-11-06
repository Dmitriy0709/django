from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Order, OrderItem


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования товаров
    Поле created_by НЕ включено (устанавливается в представлении)
    """

    class Meta:
        model = Product
        # Поля, включённые в форму (created_by устанавливается в представлении)
        fields = ['name', 'description', 'price', 'quantity', 'image', 'is_active']
        widgets = {
            # Название товара
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название товара'
            }),
            # Описание товара
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Описание товара'
            }),
            # Цена товара
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            # Количество товара
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            # Изображение товара
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            # Активен ли товар (флажок)
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_price(self):
        """
        Проверка что цена положительная
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена должна быть положительной.')
        return price

    def clean_quantity(self):
        """
        Проверка что количество неотрицательное
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError('Количество должно быть неотрицательным.')
        return quantity


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказов
    """

    class Meta:
        model = Order
        # Редактируется только статус заказа
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class OrderItemForm(forms.ModelForm):
    """
    Форма для создания и редактирования предметов в заказе
    """

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            # Выбор товара из списка
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            # Количество товара
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
            # Цена за единицу
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }

    def clean_quantity(self):
        """
        Проверка что количество больше нуля
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError('Количество должно быть больше нуля.')
        return quantity

    def clean_price(self):
        """
        Проверка что цена неотрицательная
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена должна быть неотрицательной.')
        return price
