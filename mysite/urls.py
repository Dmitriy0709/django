from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ-панель Django
    path('admin/', admin.site.urls),

    # Маршруты приложения аутентификации (ИЗМЕНЁН ПУТЬ НА accounts)
    path('accounts/', include('myauth.urls')),

    # Маршруты приложения req (если есть)
    path('req/', include('req.urls')),

    # Маршруты приложения магазина
    path('shop/', include('shopapp.urls')),
]

# Подключение статических и медиа файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
