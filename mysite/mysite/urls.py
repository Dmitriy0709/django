"""
URL configuration for mysite project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# URL без интернационализации (документация API)
urlpatterns = [
    path('req/', include('requestdataapp.urls')),
]

# API Schema and Documentation
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# URL с интернационализацией (admin и shopapp)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    path('blog/', include('blogapp.urls')),
    path("sitemap.xml", sitemap,
         {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap",
         ),
    path('', TemplateView.as_view(template_name='myauth/index.html'), name='index'),
)

# Django Debug Toolbar (только в DEBUG режиме)
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

    urlpatterns.extend(
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
