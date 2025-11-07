from django.urls import path
from . import views

# Пространство имён для приложения
app_name = 'shopapp'

urlpatterns = [
    # ========== ТОВАРЫ ==========

    # Главная страница магазина (список всех товаров)
    path('', views.ProductListView.as_view(), name='product_list'),

    # Детали товара
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Создание нового товара
    # Требует: аутентификации + разрешения 'shopapp.can_create_product'
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),

    # Редактирование товара
    # Требует: аутентификации + разрешения 'shopapp.can_edit_product' + авторства
    path('product/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_update'),

    # Удаление товара
    # Требует: аутентификации + разрешения 'shopapp.can_delete_product' + авторства
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # ========== ЗАКАЗЫ ==========

    # Список заказов пользователя
    path('orders/', views.OrderListView.as_view(), name='order_list'),

    # Детали заказа
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
