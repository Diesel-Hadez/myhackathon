from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('radar_chart', views.radar_chart, name='radar_chart'),
]
