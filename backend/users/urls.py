from django.urls import path
from .views import (
    login_view,
    logout_view,
    dashboard,
    register_view,
    update_profile,
    user_profile
)

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('dashboard/', dashboard),
    path('register/', register_view),

    # ✅ PROFILE API
    path('profile/', user_profile),
    path('profile/update/', update_profile),
]