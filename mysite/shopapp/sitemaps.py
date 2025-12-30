from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product

class ShopSitemap(Sitemap):
    """Sitemap для товаров магазина"""
    changefreq = 'weekly'
    priority = 0.8


def items(self):
    """Возвращает все товары"""
    return Product.objects.all()


def lastmod(self, item):
    """Возвращает дату последнего обновления товара"""
    return item.updated_at


def location(self, item):
    """Возвращает URL товара"""
    return item.get_absolute_url()
