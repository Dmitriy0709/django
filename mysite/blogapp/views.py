from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
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
    title = _("Последние статьи")
    description = _("Последние статьи из нашего блога")

    def link(self):
        # Используем статический путь для Feed link()
        return "/blog/articles/"

    def items(self):
        # ИСПРАВЛЕНО: используем 'pub_date' вместо 'published_at'
        return Article.objects.filter(
            pub_date__isnull=False
        ).order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        # ИСПРАВЛЕНО: используем правильное имя URL-паттерна 'article'
        return reverse("blogapp:article", kwargs={"pk": item.pk})

    def item_pubdate(self, item):
        return item.pub_date
