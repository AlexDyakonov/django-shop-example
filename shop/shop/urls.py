from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from shop import settings
from django.conf.urls.i18n import i18n_patterns

from core.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path('user/', include('userauths.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = pageNotFound