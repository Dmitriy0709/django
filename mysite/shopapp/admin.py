import csv
import json
from xml.etree import ElementTree as ET
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import format_html
from .models import Product, Order, ProductImage
from .forms import OrderCSVImportForm


class ProductImageInline(admin.TabularInline):
    """Встроенный редактор изображений товара"""
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_by', 'created_at', 'archived')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'price', 'archived')
    inlines = [ProductImageInline]
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'price')
        }),
        ('Media', {
            'fields': ('preview',)
        }),
        ('System', {
            'fields': ('created_by', 'created_at', 'updated_at', 'archived'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливает created_by при создании"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'delivery_address', 'created_at', 'import_button')
    search_fields = ('user__username', 'delivery_address', 'promocode')
    list_filter = ('created_at', 'status', 'updated_at')
    filter_horizontal = ('products',)
    readonly_fields = ('created_at', 'updated_at', 'get_total_price')

    change_list_template = 'shopapp/orders_changelist.html'

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'delivery_address', 'promocode')
        }),
        ('Products', {
            'fields': ('products',)
        }),
        ('Attachments', {
            'fields': ('receipt',)
        }),
        ('Total', {
            'fields': ('get_total_price',),
            'classes': ('wide',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def order_number(self, obj):
        """Отображает номер заказа"""
        return f"Order #{obj.pk}"

    order_number.short_description = "Order Number"

    def import_button(self, obj):
        """Добавляет кнопку импорта в список"""
        return format_html(
            '<a class="button" href="{}">Import Orders</a>',
            reverse('admin:shopapp_order_import_csv')
        )

    import_button.short_description = 'Actions'

    def get_urls(self):
        """Добавляет новый URL для импорта CSV"""
        urls = super().get_urls()
        custom_urls = [
            path(
                'import-csv/',
                self.admin_site.admin_view(self.import_csv),
                name='shopapp_order_import_csv'
            ),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        """Обработка импорта CSV/JSON/XML файла"""
        if request.method == 'POST':
            form = OrderCSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']
                file_extension = csv_file.name.split('.')[-1].lower()

                try:
                    if file_extension == 'csv':
                        self._import_csv(csv_file)
                    elif file_extension == 'json':
                        self._import_json(csv_file)
                    elif file_extension == 'xml':
                        self._import_xml(csv_file)

                    self.message_user(request, 'Orders imported successfully!')
                    return redirect('admin:shopapp_order_changelist')

                except Exception as e:
                    self.message_user(request, f'Error: {str(e)}', level='ERROR')
        else:
            form = OrderCSVImportForm()

        return render(
            request,
            'admin/csv_form.html',
            {'form': form, 'title': 'Import Orders'}
        )

    def _import_csv(self, csv_file):
        """Импорт из CSV файла"""
        csv_file.seek(0)
        reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())

        for row in reader:
            # Создаем заказ
            order = Order.objects.create(
                user_id=int(row.get('user_id', 1)),
                delivery_address=row.get('delivery_address', 'Not specified'),
                promocode=row.get('promocode', ''),
                status=row.get('status', 'pending')
            )

            # Добавляем товары, если есть product_ids
            if 'product_ids' in row and row['product_ids']:
                product_ids = [int(pid.strip()) for pid in row['product_ids'].split(',')]
                order.products.set(product_ids)

    def _import_json(self, json_file):
        """Импорт из JSON файла"""
        json_file.seek(0)
        data = json.load(json_file)

        # Если это список объектов
        if isinstance(data, list):
            orders_data = data
        # Если это объект с ключом 'orders'
        elif isinstance(data, dict) and 'orders' in data:
            orders_data = data['orders']
        else:
            raise ValueError('Invalid JSON format')

        for order_data in orders_data:
            order = Order.objects.create(
                user_id=int(order_data.get('user_id', 1)),
                delivery_address=order_data.get('delivery_address', 'Not specified'),
                promocode=order_data.get('promocode', ''),
                status=order_data.get('status', 'pending')
            )

            if 'product_ids' in order_data:
                order.products.set(order_data['product_ids'])

    def _import_xml(self, xml_file):
        """Импорт из XML файла"""
        xml_file.seek(0)
        root = ET.fromstring(xml_file.read())

        for order_elem in root.findall('order'):
            order = Order.objects.create(
                user_id=int(order_elem.findtext('user_id', 1)),
                delivery_address=order_elem.findtext('delivery_address', 'Not specified'),
                promocode=order_elem.findtext('promocode', ''),
                status=order_elem.findtext('status', 'pending')
            )

            product_ids_elem = order_elem.find('product_ids')
            if product_ids_elem is not None:
                product_ids = [int(pid) for pid in product_ids_elem.text.split(',') if pid.strip()]
                order.products.set(product_ids)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'description')
    search_fields = ('product__name', 'description')
    list_filter = ('product',)
