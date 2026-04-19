from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ STORE APP
    path('', include('store.urls')),

    # APIs
    path('api/products/', include('backend.products.urls')),
    path('api/orders/', include('backend.orders.urls')),
    path('api/users/', include('backend.users.urls')),
    path('api/cart/', include('backend.cart.urls')),
    path('api/wishlist/', include('backend.wishlist.urls')),
    path('api/contact/', include('backend.contact.urls')),
    path('api/wishlist/', include('backend.wishlist.urls')),
]

# ✅ MEDIA FIX (VERY IMPORTANT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)