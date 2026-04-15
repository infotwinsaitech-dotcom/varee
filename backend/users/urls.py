from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard,
    register_view,
    user_profile   # 🔥 ADD
)

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard),
    path('register/', register_view),

    # ✅ PROFILE API
    path('profile/', user_profile),
]