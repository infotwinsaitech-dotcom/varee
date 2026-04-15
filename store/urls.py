from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),

    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('home/', views.home, name='home'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    path('cart/', views.cart_page, name='cart'),
    path('orders/', views.orders_page, name='orders'),

    path('products/', TemplateView.as_view(template_name="products listing filter.html")),
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),

    path('checkout/', views.checkout_page),

    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('order-detail/<int:id>/', views.order_detail, name='order_detail'),
    path('order-tracking/<int:id>/', views.order_tracking, name='order_tracking'),

    # 🔥 SEARCH
    path('search/', views.search_products, name='search'),

    # EXTRA
    path('privacy/', views.privacy, name='privacy'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),
]