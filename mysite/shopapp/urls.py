from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product list
    path('', views.ProductListView.as_view(), name='product_list'),

    # Product detail
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Product CRUD
    path('create/', views.CreateProductView.as_view(), name='create_product'),
    path('product/<int:pk>/edit/', views.EditProductView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),

    # API
    path('api/create/', views.create_product_api, name='create_product_api'),
]