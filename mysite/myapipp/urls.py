from django.urls import path

from .views import hello_world_view


app_name = "myapipp"

urlpatterns = [
    path("hello/", hello_world_view, name="hello"),
]
