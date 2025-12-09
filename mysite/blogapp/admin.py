"""
Админ-панель для приложения blogapp.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Author, Category, Tag, Article


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Author.
    """
    list_display = ['name', 'created_at']
    search_fields = ['name', 'bio']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Category.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Tag.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Админ-интерфейс для модели Article.
    """
    list_display = ['title', 'author', 'category', 'pub_date', 'tag_count']
    list_filter = ['pub_date', 'category', 'author']
    search_fields = ['title', 'content', 'author__name']
    readonly_fields = ['pub_date', 'updated_at']
    fieldsets = (
        (_('Main Information'), {
            'fields': ('title', 'author', 'category')
        }),
        (_('Content'), {
            'fields': ('content',)
        }),
        (_('Tags and Dates'), {
            'fields': ('tags', 'pub_date', 'updated_at')
        }),
    )

    def tag_count(self, obj):
        """
        Отображает количество тегов для статьи.
        """
        return obj.tags.count()
    tag_count.short_description = _('Tags count')
