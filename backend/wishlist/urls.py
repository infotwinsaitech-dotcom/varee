from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_list),
    path('add/<int:product_id>/', views.add_to_wishlist),
    path('remove/<int:product_id>/', views.remove_from_wishlist),
]