"""
Представления для приложения blogapp.
"""
from django.contrib.syndication.views import Feed
from django.views.generic import ListView
from django.db.models import Prefetch
from django.urls import reverse, reverse_lazy

from .models import Article


class ArticleListView(ListView):
    """
    Представление для отображения списка всех статей с оптимизацией запросов.

    Используется:
    - select_related для подгрузки автора и категории (ForeignKey)
    - prefetch_related для подгрузки тегов (ManyToMany)
    - defer для исключения поля content из основного запроса
    """
    model = Article
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        """
        Оптимизирует запрос к БД для избежания N+1 проблемы.
        """
        return Article.objects.select_related(
            'author',  # Подгрузка автора (ForeignKey)
            'category',  # Подгрузка категории (ForeignKey)
        ).prefetch_related(
            'tags',  # Подгрузка тегов (ManyToMany)
        ).defer(
            'content',  # Исключаем большое поле content из запроса
        ).all()


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"

    def link(self):
        # ✅ Верните URL списка статей
        return reverse("blogapp:article-list")

    def items(self):
        return (
            Article.objects.filter(
                pub_date__isnull=False  # ✅ ИСПРАВЛЕНО: pub_date вместо published_at
            )
            .order_by("-pub_date")[:5]  # ✅ ИСПРАВЛЕНО: pub_date вместо published_at
        )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]  # ✅ ИЗМЕНЕНО: content вместо body

    def item_link(self, item: Article):
        return reverse("blogapp:article", kwargs={"pk": item.pk})
