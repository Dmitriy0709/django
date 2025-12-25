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
        return "/blog/articles/"

    def items(self):
        return Article.objects.filter(
            pub_date__isnull=False
        ).order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        """Расширенное описание с автором и датой"""
        # Работает с обеими моделями: Author (name) и User (get_full_name)
        author_name = None

        # Сначала проверяем поле 'name' (для кастомной Author)
        if hasattr(item.author, 'name'):
            author_name = item.author.name
        # Потом проверяем метод 'get_full_name' (для User)
        elif hasattr(item.author, 'get_full_name'):
            full_name = item.author.get_full_name()
            if full_name:
                author_name = full_name
        # Если ничего не подошло, берём username
        if not author_name:
            author_name = getattr(item.author, 'username', 'Неизвестный автор')

        pub_date = item.pub_date.strftime('%d.%m.%Y %H:%M')

        return f"""
        <p><strong>Автор:</strong> {author_name}</p>
        <p><strong>Дата публикации:</strong> {pub_date}</p>
        <div>{item.content}</div>
        """

    def item_link(self, item):
        return reverse("blogapp:article", kwargs={"pk": item.pk})

    def item_pubdate(self, item):
        return item.pub_date
