"""
Модели для приложения blogapp (блог).
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Author(models.Model):
    """
    Модель автора статьи.
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Author name')
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Biography')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категории статьи.
    """
    name = models.CharField(
        max_length=40,
        verbose_name=_('Category name')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Description')
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель тега для статьи.
    """
    name = models.CharField(
        max_length=20,
        verbose_name=_('Tag name'),
        unique=True
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Модель статьи в блоге.
    """
    title = models.CharField(
        max_length=200,
        verbose_name=_('Title')
    )
    content = models.TextField(
        verbose_name=_('Content')
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Publication date')
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name=_('Author')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name=_('Category')
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True,
        verbose_name=_('Tags')
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-pub_date']
        indexes = [
            models.Index(fields=['-pub_date']),
            models.Index(fields=['author']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk": self.pk})