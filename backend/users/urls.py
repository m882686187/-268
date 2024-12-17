# backend/users/urls.py
from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),  # 当前用户信息
]
