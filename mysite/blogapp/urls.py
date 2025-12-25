"""
URL configuration for blogapp.
"""
from django.urls import path
from . import views
from .views import LatestArticlesFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('articles/latest/feed/', LatestArticlesFeed(), name="articles-feed"),
]
