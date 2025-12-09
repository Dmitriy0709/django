"""
Management command для создания тестовых статей.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone

from blogapp.models import Author, Category, Tag, Article


class Command(BaseCommand):
    help = 'Create test articles for the blog'

    def handle(self, *args, **options):
        self.stdout.write("Creating test data for blog...")

        # Создание авторов
        author1, _ = Author.objects.get_or_create(
            name='John Doe',
            defaults={'bio': 'Experienced Django developer'}
        )
        author2, _ = Author.objects.get_or_create(
            name='Jane Smith',
            defaults={'bio': 'Web design expert'}
        )

        # Создание категорий
        category1, _ = Category.objects.get_or_create(
            name='Django',
            defaults={'description': 'Django framework articles'}
        )
        category2, _ = Category.objects.get_or_create(
            name='Python',
            defaults={'description': 'Python programming articles'}
        )

        # Создание тегов
        tag1, _ = Tag.objects.get_or_create(name='tutorial')
        tag2, _ = Tag.objects.get_or_create(name='best-practices')
        tag3, _ = Tag.objects.get_or_create(name='optimization')
        tag4, _ = Tag.objects.get_or_create(name='api')

        # Создание статей
        article1, created = Article.objects.get_or_create(
            title='Getting Started with Django',
            defaults={
                'content': 'This is a comprehensive guide to getting started with Django. '
                          'We will cover models, views, templates, and more...',
                'author': author1,
                'category': category1,
                'pub_date': timezone.now(),
            }
        )
        if created:
            article1.tags.set([tag1, tag2])

        article2, created = Article.objects.get_or_create(
            title='Django ORM Optimization Tips',
            defaults={
                'content': 'Learn how to optimize your Django ORM queries. '
                          'Discover select_related, prefetch_related, and more techniques...',
                'author': author1,
                'category': category1,
                'pub_date': timezone.now(),
            }
        )
        if created:
            article2.tags.set([tag3, tag2])

        article3, created = Article.objects.get_or_create(
            title='Building REST APIs with Django REST Framework',
            defaults={
                'content': 'A step-by-step guide to building scalable REST APIs using Django REST Framework. '
                          'Learn about serializers, viewsets, and authentication...',
                'author': author2,
                'category': category2,
                'pub_date': timezone.now(),
            }
        )
        if created:
            article3.tags.set([tag4, tag1, tag2])

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))
