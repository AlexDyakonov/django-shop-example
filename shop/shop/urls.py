from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from shop import settings
from django.conf.urls.i18n import i18n_patterns

from core.views import pageNotFound, add_to_cart, remove_from_cart, update_cart_item, coinbase_webhook, create_payment, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('i18n/', include('django.conf.urls.i18n')),
    path('add-to-cart', add_to_cart, name="add-to-cart"),
    path('remove-from-cart', remove_from_cart, name="remove-from-cart"),
    path('update-cart-item', update_cart_item, name="update-cart-item"),
    path('coinbase-webhook', coinbase_webhook, name='coinbase-webhook'),
    path('payment', create_payment, name="payment"),
]

urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path('user/', include('userauths.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

handler404 = pageNotFound