from django.urls import path
from .views import *

urlpatterns = [
    path('add/', add_to_wishlist),
    path('', get_wishlist),
    path('remove/<int:product_id>/', remove_from_wishlist),
]