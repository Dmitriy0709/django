from django.contrib import admin
from .models import Product, Category, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Product
    """
    # Поля, отображаемые в списке товаров
    list_display = ('name', 'price', 'quantity', 'created_by', 'is_active', 'created_at')

    # Фильтры на странице списка
    list_filter = ('is_active', 'created_at', 'created_by')

    # Поля для поиска
    search_fields = ('name', 'description')

    # Поля, которые нельзя редактировать
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    # Организация полей в группы
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price', 'quantity', 'image')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Метаданные', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # Свернуть по умолчанию
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Переопределение метода сохранения для автоматического
        установления created_by при создании товара
        """
        if not change:  # Если это новый товар (не редактирование)
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """
        Сделать поле created_by только для чтения при редактировании
        """
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:  # Если редактируем существующий объект
            readonly.append('created_by')
        return readonly


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Category
    """
    # Поля, отображаемые в списке
    list_display = ('name', 'created_at')

    # Поля для поиска
    search_fields = ('name', 'description')

    # Порядок сортировки
    ordering = ('name',)


class OrderItemInline(admin.TabularInline):
    """
    Встроенный редактор для модели OrderItem
    Позволяет редактировать товары в заказе прямо со страницы заказа
    """
    model = OrderItem
    # Количество пустых форм для добавления товаров
    extra = 1
    # Поля, отображаемые в таблице
    fields = ('product', 'quantity', 'price')
    # Поля, которые нельзя редактировать
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Order
    """
    # Поля, отображаемые в списке заказов
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')

    # Фильтры на странице списка
    list_filter = ('status', 'created_at', 'user')

    # Поля для поиска
    search_fields = ('user__username', 'user__email')

    # Поля, которые нельзя редактировать
    readonly_fields = ('created_at', 'updated_at', 'user')

    # Организация полей в группы
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status')
        }),
        ('Сумма', {
            'fields': ('total_amount',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Свернуть по умолчанию
        }),
    )

    # Встроенное редактирование товаров в заказе
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        """
        Сделать поле user только для чтения при редактировании заказа
        """
        readonly = list(super().get_readonly_fields(request, obj))
        if obj:  # Если редактируем существующий заказ
            readonly.append('user')
        return readonly
