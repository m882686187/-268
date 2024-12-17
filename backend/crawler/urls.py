# crawler/urls.py
from django.urls import path
from .views import attractions_view, download_excel

urlpatterns = [
    path('attractions/', attractions_view, name='attractions'),
    path('download-excel/', download_excel, name='download_excel'),  # 新增的下载Excel路由
]
