"""
URL configuration for blogapp.
"""
from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', views.LatestArticlesFeed(), name='latest-feed'),
]


