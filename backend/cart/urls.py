from django.urls import path
from .views import cart_list, cart_detail

urlpatterns = [
    path('', cart_list),
    path('<int:id>/', cart_detail),
]