"""
Представления для приложения blogapp.
"""
from django.views.generic import ListView
from django.db.models import Prefetch

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
