from django.urls import path
from .views import dashboard_api

urlpatterns = [
    path('', dashboard_api),
]