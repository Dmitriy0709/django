from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Product


class LatestProductsFeed(Feed):
    """RSS Feed с последними товарами"""
    title = "Latest Products"
    link = "/products/"
    description = "Updates on latest products in our shop"

    def items(self):
        """Возвращает последние 10 товаров"""
        return Product.objects.all().order_by('-created_at')[:10]

    def item_title(self, item):
        """Название товара в RSS"""
        return item.name

    def item_description(self, item):
        """Описание товара в RSS"""
        return item.description

    def item_link(self, item):
        """Ссылка на товар в RSS"""
        return item.get_absolute_url()

    def item_pubdate(self, item):
        """Дата публикации товара в RSS"""
        return item.created_at
