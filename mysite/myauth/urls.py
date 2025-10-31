from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (get_cookie_view,
                    set_cookie_view,
                    set_session_view,
                    get_session_view,
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    )

app_name = "myauth"

urlpatterns = [
    # Стандартные Django auth views
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
    ), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),

    # Регистрация
    path('register/', RegisterView.as_view(), name='register'),

    # Профиль пользователя
    path('about-me/', AboutMeView.as_view(), name='about-me'),

    # Cookie и session views (если нужны)
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
]
