from django.contrib.auth.views import LoginView
from django.urls import path

from .views import login_view

app_name = "myauth"

urlpatterns = [
    #path("login/", login_view, name="login"),
    path("login/", LoginView.as_view(template_name="myauth/login.html", redirect_authenticated_user=True), name="login"),
]
