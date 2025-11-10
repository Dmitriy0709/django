from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'myauth'

urlpatterns = [
    # Authentication
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # Cookie operations
    path('set-cookie/', views.set_cookie_view, name='set_cookie'),
    path('get-cookie/', views.get_cookie_view, name='get_cookie'),

    # Session operations
    path('set-session/', views.set_session_view, name='set_session'),
    path('get-session/', views.get_session_view, name='get_session'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]
