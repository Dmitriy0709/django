from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductViewSet

app_name = 'shopapp'

routers = DefaultRouter()
routers.register("products", ProductViewSet)


urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path("api/", include(routers.urls)),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/export/', views.ProductsExportView.as_view(), name='products-export'),

    # URLs для заказов
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/export/', views.OrdersExportView.as_view(), name='orders-export'),
]
r