from django.urls import path

from .views import process_get_view

app_name = "shopapp"

urlpatterns = [
    path("get/", process_get_view, name="get-vew"),
]
