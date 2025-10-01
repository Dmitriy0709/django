from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import GroupForm
from .forms import ProductForm, OrderForm
from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 3999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    model = Product
    context_object_name = "products"

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context["products"] = Product.objects.all()
    #    return context

#def products_list(request:HttpRequest):
#    context = {
#        "products": Product.objects.all(),
#    }
#    return render(request, 'shopapp/products-list.html', context=context)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/products-details.html'
    model = Product
    context_object_name = "product"
    #def get(self, request: HttpRequest, pk: int) -> HttpResponse:
    #    product = get_object_or_404(Product, pk=pk)
    #    context = {
    #        "product": product,
    #    }
    #    return render(request, "shopapp/products-details.html", context=context)


class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")


#def create_product(request: HttpRequest) -> HttpResponse:
#    if request.method == "POST":
#        form = ProductForm(request.POST)
#        if form.is_valid():
#            #name = form.cleaned_data["name"]
#            #price = form.cleaned_data["price"]
#            #Product.objects.create(**form.cleaned_data)
#            form.save()
#            url = reverse("shopapp:products_list")
#            return redirect(url)

#    else:
#        form = ProductForm
#    context = {
#        "form": form,
#    }

#    return render(request, "shopapp/create-product.html", context=context)


#def orders_list(request:HttpRequest):
#    context = {
#        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#    }
#    return render(request,'shopapp/orders-list.html', context=context)


class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("shopapp:orders_list"))
    else:
        form = OrderForm()
    return render(request, "shopapp/create-order.html", {"form": form})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:product_list")

class OrdersListView(ListView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )


class OrderDetailView(DetailView):
    queryset = (
        Order.objects.select_related("user").prefetch_related("products")
    )

