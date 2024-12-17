# myapp/urls.py

from django.urls import path
from .views import BarChart
from .views import LineChart
from .views import PieChart
from  .views import BoxChart
from .views import ScatterPlot
from .views import RadarChart
urlpatterns = [
    path('api/BarChart/', BarChart, name='BarChart'),
    path('api/LineChart/', LineChart, name='LineChart'),
    path('api/PieChart/', PieChart, name='PieChart'),
    path('api/BoxChart/',BoxChart, name='BoxChart'),
    path('api/ScatterPlot/',ScatterPlot, name='ScatterPlot'),
    path('api/RadarChart/',RadarChart, name='RadarChart'),
]
