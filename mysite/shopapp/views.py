from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView,
    DeleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Product, Category, Order, OrderItem
from .forms import ProductForm


# ========== СПИСОК ТОВАРОВ ==========

class ProductListView(ListView):
    """
    Представление для отображения списка всех активных товаров
    """
    model = Product
    template_name = 'shopapp/product_list.html'
    context_object_name = 'products'
    # Количество товаров на странице
    paginate_by = 12

    def get_queryset(self):
        """Получить только активные товары"""
        return Product.objects.filter(is_active=True).select_related('created_by')


# ========== ДЕТАЛИ ТОВАРА ==========

class ProductDetailView(DetailView):
    """
    Представление для отображения детальной информации о товаре
    """
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """Получить только активные товары"""
        return Product.objects.filter(is_active=True)


# ========== СОЗДАНИЕ ТОВАРА ==========

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания нового товара
    Требует:
    - Аутентификации (LoginRequiredMixin)
    - Разрешения 'can_create_product' (PermissionRequiredMixin)

    Автоматически присваивает текущего пользователя как автора товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    # URL для редиректа неавторизованных пользователей
    login_url = 'myauth:login'
    # ========== КЛЮЧЕВОЙ ПАРАМЕТР: Требуемое разрешение
    permission_required = 'shopapp.can_create_product'

    def form_valid(self, form):
        """
        Переопределение метода form_valid
        Устанавливает текущего пользователя как автора товара
        """
        # ========== УСТАНОВКА АВТОРА
        form.instance.created_by = self.request.user

        # Добавление сообщения об успехе
        messages.success(self.request, 'Товар успешно создан!')

        # ========== ИСПОЛЬЗОВАНИЕ super() для сохранения
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка ошибок формы"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}: {error}')
        return super().form_invalid(form)

    def get_success_url(self):
        """Редирект на страницу товара после создания"""
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


# ========== РЕДАКТИРОВАНИЕ ТОВАРА ==========

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для редактирования товара

    Ограничения доступа:
    - Суперпользователь может редактировать любой товар
    - Остальные пользователи могут редактировать товар ТОЛЬКО если:
      1) У них есть разрешение 'can_edit_product'
      2) Они являются автором товара
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    login_url = 'myauth:login'

    def get_queryset(self):
        """
        Фильтрация товаров на основе прав пользователя
        Суперпользователь видит все товары
        Остальные пользователи видят только свои товары
        """
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(created_by=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """
        Проверка разрешений перед редактированием товара
        """
        product = self.get_object()

        # ========== ПРОВЕРКА 1: Суперпользователь может всегда
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # ========== ПРОВЕРКА 2: Разрешение на редактирование
        has_permission = request.user.has_perm('shopapp.can_edit_product')

        # ========== ПРОВЕРКА 3: Является ли автором товара
        is_author = product.created_by == request.user

        # ========== ПРОВЕРКА 4: ОБЕ УСЛОВИЯ ДОЛЖНЫ БЫТЬ ВЫПОЛНЕНЫ
        if not (has_permission and is_author):
            messages.error(
                request,
                'У вас нет разрешения редактировать этот товар.'
            )
            return HttpResponseForbidden('Доступ запрещён.')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        messages.success(self.request, 'Товар успешно обновлён!')
        return super().form_valid(form)

    def get_success_url(self):
        """Редирект на страницу товара после обновления"""
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


# ========== УДАЛЕНИЕ ТОВАРА ==========

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления товара
    Аналогичные ограничения как при редактировании товара:
    - Только суперпользователь или пользователь с разрешением
      'can_delete_product' и являющийся автором может удалить товар
    """
    model = Product
    template_name = 'shopapp/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    login_url = 'myauth:login'

    def get_queryset(self):
        """Фильтрация товаров при удалении"""
        if self.request.user.is_superuser:
            return Product.objects.all()
        return Product.objects.filter(created_by=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """Проверка разрешений перед удалением"""
        product = self.get_object()

        # Если пользователь НЕ суперпользователь
        if not request.user.is_superuser:
            # Проверяем наличие разрешения на удаление
            has_permission = request.user.has_perm('shopapp.can_delete_product')
            # Проверяем является ли пользователь автором
            is_author = product.created_by == request.user

            # Если нет разрешения ИЛИ не является автором
            if not (has_permission and is_author):
                messages.error(
                    request,
                    'У вас нет разрешения удалить этот товар.'
                )
                return HttpResponseForbidden('Доступ запрещён.')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление товара с выводом сообщения об успехе"""
        messages.success(request, 'Товар успешно удалён!')
        return super().delete(request, *args, **kwargs)


# ========== СПИСОК ЗАКАЗОВ ==========

class OrderListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения заказов пользователя
    """
    model = Order
    template_name = 'shopapp/order_list.html'
    context_object_name = 'orders'
    login_url = 'myauth:login'

    def get_queryset(self):
        """Получить только заказы текущего пользователя"""
        return Order.objects.filter(user=self.request.user).prefetch_related('items')


# ========== ДЕТАЛИ ЗАКАЗА ==========

class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей заказа
    Пользователи могут видеть только свои заказы
    """
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'
    login_url = 'myauth:login'

    def get_queryset(self):
        """Получить только заказы текущего пользователя"""
        return Order.objects.filter(user=self.request.user)
