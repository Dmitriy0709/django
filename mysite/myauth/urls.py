from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myauth'

urlpatterns = [
    # Стандартные views из django.contrib.auth
    path('login/', auth_views.LoginView.as_view(template_name='myauth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='myauth/password_change.html'),
         name='password_change'),
    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='myauth/password_change_done.html'),
         name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='myauth/password_reset.html'),
         name='password_reset'),
    path('password-reset-done/',
         auth_views.PasswordResetDoneView.as_view(template_name='myauth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='myauth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='myauth/password_reset_complete.html'),
         name='password_reset_complete'),

    # Пользовательские views
    path('register/', views.RegisterView.as_view(), name='register'),
    path('about-me/', views.AboutMeView.as_view(), name='about-me'),

    # Cookie views
    path('cookie/get/', views.get_cookie_view, name='cookie-get'),
    path('cookie/set/', views.set_cookie_view, name='cookie-set'),

    # Session views
    path('session/get/', views.get_session_view, name='session-get'),
    path('session/set/', views.set_session_view, name='session-set'),
]