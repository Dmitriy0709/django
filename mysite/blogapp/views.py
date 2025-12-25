from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article


class ArticleListView(ListView):
    """Список всех статей"""
    model = Article
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(
            pub_date__isnull=False
        ).order_by('-pub_date')


class ArticleDetailView(DetailView):
    """Детальный просмотр статьи"""
    model = Article
    template_name = 'blogapp/article_detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Article.objects.filter(pub_date__isnull=False)


class LatestArticlesFeed(Feed):
    """RSS-лента последних статей"""
    title = "Последние статьи"
    description = "Последние статьи из нашего блога"

    def link(self):
        # Возвращает ссылку на страницу списка статей
        return reverse("blogapp:articles")

    def items(self):
        # Исправлено: используем 'pub_date' вместо 'published_at'
        return Article.objects.filter(
            pub_date__isnull=False
        ).order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        # Исправлено: используем правильное имя URL-паттерна 'article'
        return reverse("blogapp:article", kwargs={"pk": item.pk})

    def item_pubdate(self, item):
        return item.pub_date
