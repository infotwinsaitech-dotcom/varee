from django.urls import path
from .views import (
    create_payment,
    get_orders,
    place_order,
    cancel_order,
    verify_payment,
    get_order_detail   # ✅ ADD THIS
)

urlpatterns = [
    path('', get_orders),
    path('place/', place_order),
    path('cancel/<int:order_id>/', cancel_order),
    path('create-payment/', create_payment),
    path('verify-payment/', verify_payment),

    # ✅ ORDER TRACKING
    path('<int:order_id>/', get_order_detail),
    
]