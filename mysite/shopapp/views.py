from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Order, ProductImage
from .forms import ProductForm
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name",
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "name",
        "price",
        "discount",
    ]


class ProductListView(ListView):
    """
    Представление для отображения списка всех продуктов.
    """
    model = Product
    template_name = 'shopapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProductDetailView(DetailView):
    """
    Представление для отображения деталей продукта.
    """
    #model = Product
    queryset = Product.objects.prefetch_related("images")
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового продукта.
    Только пользователи с разрешением на создание могут создавать продукты.
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:product_list')
    login_url = settings.LOGIN_URL

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('shopapp.can_create_product'):
            raise Http404("You don't have permission to create products")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Product'
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Представление для редактирования продукта.
    Ограничение: суперпользователь или автор с разрешением на редактирование.
    """
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'
    success_url = reverse_lazy('shopapp:product_list')
    login_url = settings.LOGIN_URL

    def test_func(self):
        product = self.get_object()
        # Суперпользователь может редактировать всегда
        if self.request.user.is_superuser:
            return True
        # Остальные - только если они автор и имеют разрешение
        return (product.created_by == self.request.user and
                self.request.user.has_perm('shopapp.can_edit_product'))

    def handle_no_permission(self):
        raise Http404("You don't have permission to edit this product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Product'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Представление для удаления продукта.
    """
    model = Product
    template_name = 'shopapp/product_confirm_delete.html'
    success_url = reverse_lazy('shopapp:product_list')
    login_url = settings.LOGIN_URL

    def test_func(self):
        product = self.get_object()
        if self.request.user.is_superuser:
            return True
        return (product.created_by == self.request.user and
                self.request.user.has_perm('shopapp.can_delete_product'))

    def handle_no_permission(self):
        raise Http404("You don't have permission to delete this product")


class OrderListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка заказов текущего пользователя.
    """
    model = Order
    template_name = 'shopapp/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        # Показываем только заказы текущего пользователя
        return Order.objects.filter(user=self.request.user).prefetch_related('products')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей заказа.
    """
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'
    login_url = settings.LOGIN_URL

    def get_queryset(self):
        # Пользователь может видеть только свои заказы
        return Order.objects.filter(user=self.request.user)


@method_decorator(user_passes_test(lambda user: user.is_staff), name='dispatch')
class OrdersExportView(ListView):
    """
    Представление для экспорта всех заказов в JSON.
    Доступ только для is_staff пользователей.
    """
    model = Order

    def get_queryset(self):
        # Получаем все заказы с подгрузкой пользователей и продуктов
        return Order.objects.select_related('user').prefetch_related('products').order_by('pk')

    def render_to_response(self, context, **response_kwargs):
        orders = self.get_queryset()

        orders_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.pk,
                'products': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]

        return JsonResponse({'orders': orders_data})


class ProductsExportView(ListView):
    """
    Представление для экспорта всех продуктов в JSON.
    """
    model = Product

    def render_to_response(self, context, **response_kwargs):
        products = Product.objects.order_by('pk').all()

        products_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived,
            }
            for product in products
        ]

        return JsonResponse({'products': products_data})
