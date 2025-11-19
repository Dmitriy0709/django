"""
URL configuration for myauth app.
"""
from django.urls import path
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views
from .views import FooBarView

app_name = 'accounts'  # ← ИЗМЕНИТЕ ЗДЕСЬ (было 'myauth', теперь 'accounts')

urlpatterns = [
    # Аутентификация
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Cookies
    path('set-cookie/', views.set_cookie_view, name='set_cookie'),
    path('get-cookie/', views.get_cookie_view, name='get_cookie'),

    # Session
    path('set-session/', views.set_session_view, name='set_session'),
    path('get-session/', views.get_session_view, name='get_session'),

    # Профиль
    path('profile/', views.profile_view, name='profile'),

    # Смена пароля
    path('password-change/', PasswordChangeView.as_view(
        template_name='myauth/password_change.html'
    ), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='myauth/password_change_done.html'
    ), name='password_change_done'),

    # Восстановление пароля
    path('password-reset/', PasswordResetView.as_view(
        template_name='myauth/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='myauth/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='myauth/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='myauth/password_reset_complete.html'
    ), name='password_reset_complete'),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar")
]
