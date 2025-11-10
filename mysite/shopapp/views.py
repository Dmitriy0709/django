from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    """View to list all products"""
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')


class ProductDetailView(DetailView):
    """View to display product details"""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'id'
    slug_url_kwarg = 'pk'


class CreateProductView(LoginRequiredMixin, CreateView):
    """View to create a new product"""
    model = Product
    form_class = ProductForm
    template_name = 'shop/create_product.html'
    success_url = reverse_lazy('shop:product_list')
    login_url = 'myauth:login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('shop.can_create_product'):
            return HttpResponseForbidden("You don't have permission to create products")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Bind the product to the current user"""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EditProductView(LoginRequiredMixin, UpdateView):
    """View to edit a product"""
    model = Product
    form_class = ProductForm
    template_name = 'shop/edit_product.html'
    success_url = reverse_lazy('shop:product_list')
    login_url = 'myauth:login'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Check permissions
        if not product.can_edit(request.user):
            return HttpResponseForbidden("You don't have permission to edit this product")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Bind the product to the current user"""
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DeleteProductView(LoginRequiredMixin, DeleteView):
    """View to delete a product"""
    model = Product
    template_name = 'shop/confirm_delete_product.html'
    success_url = reverse_lazy('shop:product_list')
    login_url = 'myauth:login'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()

        # Check permissions
        if not product.can_delete(request.user):
            return HttpResponseForbidden("You don't have permission to delete this product")

        return super().dispatch(request, *args, **kwargs)


@login_required(login_url='myauth:login')
@permission_required('shop.can_create_product', raise_exception=True)
def create_product_api(request):
    """API view to create product via form"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('shop:product_detail', pk=product.id)
    else:
        form = ProductForm()

    return render(request, 'shop/create_product.html', {'form': form})
