"""
Представления для приложения shopapp.
"""
import logging
from dataclasses import field
from pickle import FALSE
from csv import DictReader, DictWriter

from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core.cache import cache
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.request import Request

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Product, Order
from .forms import ProductForm
from .serializers import ProductSerializer, OrderSerializer


log = logging.getLogger(__name__)

# ============================================
# REST API ViewSets
# ============================================

@extend_schema_view(
    list=extend_schema(
        summary="Список всех продуктов",
        description="Получить список всех продуктов с возможностью поиска и сортировки",
        parameters=[
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Поиск по названию или описанию продукта',
                examples=[
                    OpenApiExample('Поиск ноутбука', value='laptop'),
                    OpenApiExample('Поиск телефона', value='phone'),
                ]
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Сортировка результатов (name, price, created_at). Используйте "-" для обратной сортировки.',
                examples=[
                    OpenApiExample('По цене возрастание', value='price'),
                    OpenApiExample('По цене убывание', value='-price'),
                    OpenApiExample('По названию', value='name'),
                ]
            ),
        ],
        tags=['products'],
    ),
    retrieve=extend_schema(
        summary="Детали продукта",
        description="Получить подробную информацию о конкретном продукте",
        tags=['products'],
    ),
    create=extend_schema(
        summary="Создать продукт",
        description="Создать новый продукт (требуется аутентификация)",
        tags=['products'],
    ),
    update=extend_schema(
        summary="Обновить продукт",
        description="Обновить существующий продукт (требуется аутентификация)",
        tags=['products'],
    ),
    partial_update=extend_schema(
        summary="Частично обновить продукт",
        description="Частично обновить существующий продукт (требуется аутентификация)",
        tags=['products'],
    ),
    destroy=extend_schema(
        summary="Удалить продукт",
        description="Удалить продукт (требуется аутентификация)",
        tags=['products'],
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с продуктами через API.

    Предоставляет CRUD операции для продуктов с поддержкой:
    - Поиска по названию и описанию
    - Сортировки по различным полям
    - Пагинации результатов
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

    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(context_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            "name",
            "price",
            "created_at",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

@extend_schema_view(
    list=extend_schema(
        summary="Список всех заказов",
        description="Получить список всех заказов с возможностью фильтрации и сортировки",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Фильтр по статусу заказа',
                enum=['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
                examples=[
                    OpenApiExample('Ожидающие', value='pending'),
                    OpenApiExample('Доставленные', value='delivered'),
                ]
            ),
            OpenApiParameter(
                name='user',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Фильтр по ID пользователя',
            ),
            OpenApiParameter(
                name='promocode',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Фильтр по промокоду',
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Сортировка результатов (created_at, updated_at, status). Используйте "-" для обратной сортировки.',
                examples=[
                    OpenApiExample('Новые первыми', value='-created_at'),
                    OpenApiExample('Старые первыми', value='created_at'),
                ]
            ),
        ],
        tags=['orders'],
    ),
    retrieve=extend_schema(
        summary="Детали заказа",
        description="Получить подробную информацию о конкретном заказе",
        tags=['orders'],
    ),
    create=extend_schema(
        summary="Создать заказ",
        description="Создать новый заказ (требуется аутентификация)",
        tags=['orders'],
    ),
    update=extend_schema(
        summary="Обновить заказ",
        description="Обновить существующий заказ (требуется аутентификация)",
        tags=['orders'],
    ),
    partial_update=extend_schema(
        summary="Частично обновить заказ",
        description="Частично обновить существующий заказ (требуется аутентификация)",
        tags=['orders'],
    ),
    destroy=extend_schema(
        summary="Удалить заказ",
        description="Удалить заказ (требуется аутентификация)",
        tags=['orders'],
    ),
)
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заказами через API.

    Предоставляет CRUD операции для заказов с поддержкой:
    - Фильтрации по статусу, пользователю, промокоду
    - Сортировки по различным полям
    - Пагинации результатов
    - Вычисления общей стоимости заказа
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
