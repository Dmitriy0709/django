"""
Представления для приложения shopapp.
"""

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpRequest, JsonResponse
from django.core.cache import cache
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Order
from .forms import ProductForm
from .serializers import ProductSerializer, OrderSerializer


# ============================================
# REST API ViewSets
# ============================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с продуктами через API.

    Доступные фильтры:
    - Поиск (search): name, description
    - Сортировка (ordering): name, price, created_at

    Примеры запросов:
    - GET /api/products/ - список всех продуктов
    - GET /api/products/?search=laptop - поиск по названию/описанию
    - GET /api/products/?ordering=price - сортировка по цене (по возрастанию)
    - GET /api/products/?ordering=-price - сортировка по цене (по убыванию)
    - POST /api/products/ - создание продукта (требуется аутентификация)
    """
    queryset = Product.objects.select_related('created_by').prefetch_related('images').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Фильтрация и поиск
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Поля для поиска
    search_fields = ['name', 'description']

    # Поля для сортировки
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['id']  # Сортировка по умолчанию


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заказами через API.

    Доступные фильтры:
    - Фильтрация (filter): status, user, promocode
    - Сортировка (ordering): created_at, updated_at, status

    Примеры запросов:
    - GET /api/orders/ - список всех заказов
    - GET /api/orders/?status=pending - фильтр по статусу
    - GET /api/orders/?user=1 - фильтр по пользователю
    - GET /api/orders/?ordering=-created_at - сортировка по дате создания (новые первыми)
    - POST /api/orders/ - создание заказа (требуется аутентификация)
    """
    queryset = Order.objects.select_related('user').prefetch_related('products').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Фильтрация и сортировка
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    # Поля для фильтрации
    filterset_fields = ['status', 'user', 'promocode']

    # Поля для сортировки
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']  # Сортировка по умолчанию (новые первыми)


# ============================================
# Traditional Django Views (HTML)
# ============================================

class ProductListView(ListView):
    """
    Представление для отображения списка продуктов.
    """
    model = Product
    template_name = 'shopapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.select_related('created_by').filter(archived=False)


class ProductDetailView(DetailView):
    """
    Представление для отображения деталей продукта.
    """
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.select_related('created_by').prefetch_related('images')


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:product_list')
    permission_required = 'shopapp.can_create_product'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для редактирования продукта.
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'

    def test_func(self):
        product = self.get_object()
        return product.can_edit(self.request.user)

    def get_success_url(self):
        return reverse_lazy('shopapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Представление для удаления продукта.
    """
    model = Product
    template_name = 'shopapp/product_confirm_delete.html'
    success_url = reverse_lazy('shopapp:product_list')

    def test_func(self):
        product = self.get_object()
        return product.can_delete(self.request.user)


class OrderListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка заказов.
    """
    model = Order
    template_name = 'shopapp/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related('products').all()
        return Order.objects.select_related('user').prefetch_related('products').filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей заказа.
    """
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related('products').all()
        return Order.objects.select_related('user').prefetch_related('products').filter(user=self.request.user)


class ProductsExportView(View):
    """
    Представление для экспорта продуктов в JSON.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = 'products_export_data'
        products_data = cache.get(cache_key)

        if products_data is None:
            products = Product.objects.select_related('created_by').order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': str(product.price),
                    'archived': product.archived,
                    'created_by': product.created_by.username,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)  # Кэшируем на 5 минут

        return JsonResponse({'products': products_data})


class OrdersExportView(View):
    """
    Представление для экспорта заказов в JSON.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related('user').prefetch_related('products').order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'user': order.user.username,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'status': order.status,
                'products': [
                    {
                        'pk': product.pk,
                        'name': product.name,
                        'price': str(product.price),
                    }
                    for product in order.products.all()
                ],
                'total_price': str(order.get_total_price()),
            }
            for order in orders
        ]

        return JsonResponse({'orders': orders_data})
