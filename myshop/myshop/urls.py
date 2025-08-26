from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls import include


urlpatterns = i18n_patterns(
 path(_('admin/'), admin.site.urls),
 path(_('cart/'), include('cart.urls', namespace='cart')),
 path(_('orders/'), include('orders.urls', namespace='orders')),
 path(_('payment/'), include('payment.urls', namespace='payment')),
 path(_('coupons/'), include('coupons.urls', namespace='coupons')),
 path('rosetta/', include('rosetta.urls')),
 path('', include('shop.urls', namespace='shop')),
)

# Language switching URL (outside i18n_patterns)
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls), # admin site

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
