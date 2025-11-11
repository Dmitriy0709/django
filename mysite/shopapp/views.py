from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import Http404

from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """
    Представление для отображения списка всех продуктов.
    """
    model = Product
    template_name = 'shopapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(DetailView):
    """
    Представление для отображения деталей продукта.
    """
    model = Product
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
    login_url = 'myauth:login'

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
    login_url = 'myauth:login'

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


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Представление для удаления продукта.
    """
    model = Product
    template_name = 'shopapp/product_confirm_delete.html'
    success_url = reverse_lazy('shopapp:product_list')
    login_url = 'myauth:login'

    def test_func(self):
        product = self.get_object()
        if self.request.user.is_superuser:
            return True
        return (product.created_by == self.request.user and
                self.request.user.has_perm('shopapp.can_delete_product'))

    def handle_no_permission(self):
        raise Http404("You don't have permission to delete this product")
