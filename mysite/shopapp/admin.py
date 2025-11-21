from django.contrib import admin
from .models import Product, Order
from .admin_mixins import ExportAsCSVMixin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    list_display = ['id', 'name', 'price', 'created_by', 'created_at', 'archived']
    list_filter = ['archived', 'created_at']
    search_fields = ['name', 'description']
    actions = ['mark_as_archived', 'export_csv']

    def mark_as_archived(self, request, queryset):
        queryset.update(archived=True)
    mark_as_archived.short_description = 'Mark selected products as archived'


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
