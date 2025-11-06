from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Пространство имён для приложения
app_name = 'myauth'

urlpatterns = [
    # ========== СТАНДАРТНЫЕ DJANGO AUTH VIEWS ==========

    # Вход в аккаунт
    # Требует шаблон: myauth/login.html
    path('login/', auth_views.LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True  # Редирект уже авторизованных пользователей
    ), name='login'),

    # Выход из аккаунта (ПОЛЬЗОВАТЕЛЬСКИЙ КЛАСС)
    # Переопределена страница перенаправления
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Смена пароля (требует аутентификации)
    # Требует шаблон: myauth/password_change.html
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='myauth/password_change.html'
    ), name='password_change'),

    # Подтверждение успешной смены пароля
    # Требует шаблон: myauth/password_change_done.html
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='myauth/password_change_done.html'
    ), name='password_change_done'),

    # Запрос на сброс пароля
    # Требует шаблон: myauth/password_reset.html
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='myauth/password_reset.html'
    ), name='password_reset'),

    # Подтверждение отправки письма для сброса пароля
    # Требует шаблон: myauth/password_reset_done.html
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='myauth/password_reset_done.html'
    ), name='password_reset_done'),

    # Подтверждение и сброс пароля (по уникальной ссылке)
    # Требует шаблон: myauth/password_reset_confirm.html
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='myauth/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Завершение сброса пароля
    # Требует шаблон: myauth/password_reset_complete.html
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='myauth/password_reset_complete.html'
    ), name='password_reset_complete'),

    # ========== COOKIES VIEWS ==========

    # Чтение cookies
    # Возвращает JSON с текущим значением cookie
    path('cookies/read/', views.read_cookies_view, name='read_cookies'),

    # Установка cookies
    # Устанавливает cookie и возвращает JSON подтверждение
    path('cookies/set/', views.set_cookies_view, name='set_cookies'),

    # ========== SESSION VIEWS ==========

    # Чтение session
    # Возвращает JSON с текущим значением session
    path('session/read/', views.read_session_view, name='read_session'),

    # Установка session
    # Устанавливает session и возвращает JSON подтверждение
    path('session/set/', views.set_session_view, name='set_session'),

    # ========== ПОЛЬЗОВАТЕЛЬСКИЕ VIEWS ==========

    # Регистрация нового пользователя
    # Требует шаблон: myauth/register.html
    path('register/', views.RegisterView.as_view(), name='register'),

    # Просмотр профиля пользователя
    # Требует аутентификации (@login_required декоратор в views)
    # Требует шаблон: myauth/profile.html
    path('profile/', views.profile_view, name='profile'),

    # Редактирование профиля пользователя
    # Требует аутентификации (@login_required декоратор в views)
    # Требует шаблон: myauth/profile_edit.html
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
