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
        title = "Blog articles (lates)"
        description = "Updates on changes and addition blog articles"
        lonk = reverse_lazy("blogapp:articles")

        def items(self):
            return (
                Article.objects.filter(
                    published_at_isnull=False)
                .order_by("-published_at")[:5]
                )

        def item_title(self, item: Article):
            return item.title

        def item_description(self, item:Article):
            return item.body[:200]

        def item_link(self, item:Article):
            return reverse("blogapp:article", kwargs={"pk": item.pk})



