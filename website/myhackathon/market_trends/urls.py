from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('radar_chart', views.radar_chart, name='radar_chart'),
    path('line_chart', views.line_chart, name="line_chart"),
    path('skills_for_job', views.job_parse, name="skills_for_job")
]
