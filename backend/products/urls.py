from django.urls import path
from .views import (
    get_products,
    get_product_detail,
    get_categories,
    add_product   # 🔥 NEW
)

urlpatterns = [
    path('', get_products),
    path('categories/', get_categories),
    path('add/', add_product),   # ✅ IMPORTANT
    path('<int:id>/', get_product_detail),
]