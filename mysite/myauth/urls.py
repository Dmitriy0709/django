from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Пространство имён для приложения
app_name = 'myauth'

urlpatterns = [
    # ========== Стандартные Django представления для аутентификации ==========

    # Вход в аккаунт
    path('login/', auth_views.LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True  # Редирект уже авторизованных пользователей
    ), name='login'),

    # Выход из аккаунта
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Смена пароля (требует аутентификации)
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='myauth/password_change.html'
    ), name='password_change'),

    # Подтверждение успешной смены пароля
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='myauth/password_change_done.html'
    ), name='password_change_done'),

    # Запрос на сброс пароля
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='myauth/password_reset.html'
    ), name='password_reset'),

    # Подтверждение отправки письма для сброса пароля
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myauth/password_reset_done.html'
    ), name='password_reset_done'),

    # Подтверждение и сброс пароля (по уникальной ссылке)
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myauth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Завершение сброса пароля
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myauth/password_reset_complete.html'
    ), name='password_reset_complete'),

    # ========== Пользовательские представления ==========

    # Регистрация нового пользователя
    path('register/', views.RegisterView.as_view(), name='register'),

    # Просмотр профиля пользователя
    # Требует аутентификации (@login_required декоратор в views)
    path('profile/', views.profile_view, name='profile'),

    # Редактирование профиля пользователя
    # Требует аутентификации (@login_required декоратор в views)
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
