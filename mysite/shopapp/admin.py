from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from werkzeug.utils import redirect

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    list_display = ['id', 'name', 'price', 'created_by', 'created_at', 'archived']
    list_filter = ['archived', 'created_at']
    search_fields = ['name', 'description']
    actions = ['mark_as_archived', 'export_csv']

    def mark_as_archived(self, request, queryset):
        queryset.update(archived=True)
    mark_as_archived.short_description = 'Mark selected products as archived'

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)

        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        products = [
            Product(**row)
            for row in reader
        ]
        Product.objects.bulk_create(products)
        self.message_user(request, "data from CSV was imported")
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = ['id', 'user', 'status', 'created_at', 'get_products_count']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'delivery_address']
    filter_horizontal = ['products']
    actions = ['export_csv']

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = 'Products Count'
