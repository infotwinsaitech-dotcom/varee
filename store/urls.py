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

    path('otp-login/', views.otp_login_page, name='otp_login'),
    path('verify-login-otp/', views.verify_login_otp, name='verify_login_otp'),

    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('orders/', views.orders_page, name='orders'),
    path('order-detail/<int:id>/', views.order_detail, name='order_detail'),
    path('order-tracking/<int:id>/', views.order_tracking, name='order_tracking'),

    
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),

    path('search/', views.search_products, name='search'),

    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

    path('settings/', views.settings_page, name='settings'),
    path('settings/security/', views.security_page, name='security'),
    path('settings/notifications/', views.notifications_page, name='notifications'),
    path('settings/preferences/', views.preferences_page, name='preferences'),

    path('success/', views.success_page, name='success'),
    path('products/', views.product_list, name='products'),
    path('verify-otp/', views.verify_otp),

]