from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ================= FRONTEND =================
    path('', views.login_view),
    path('home/', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('orders/', views.orders_page, name='orders'),
    path('order-detail/<int:id>/', views.order_detail, name='order_detail'),
    path('order-tracking/<int:id>/', views.order_tracking, name='order_tracking'),

    path('products/', views.home),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),

    path('search/', views.search_products, name='search'),

    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('terms/', views.terms),
    path('shipping/', views.shipping),
    path('sustainability/', views.sustainability),
    path('privacy/', views.privacy),
    path('contact/', views.contact),

    path('dashboard/', views.dashboard),
    path('user-dashboard/', views.user_dashboard),

    # ================= APIs =================
    path('api/products/', include('backend.products.urls')),
    path('api/orders/', include('backend.orders.urls')),
    path('api/users/', include('backend.users.urls')),
    path('api/cart/', include('backend.cart.urls')),
    path('api/wishlist/', include('backend.wishlist.urls')),
    path('api/contact/', include('backend.contact.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)