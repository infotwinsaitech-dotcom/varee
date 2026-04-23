from django.urls import path
from . import views

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
    path('product-detail/<int:id>/', views.product_detail, name='product_detail'),

    path('search/', views.search_products, name='search'),

    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),

    path('products/', views.product_list, name='products'),
]