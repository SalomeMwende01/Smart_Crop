from django.urls import path

from .views import MonitoringHealthView

urlpatterns = [
    path('health/', MonitoringHealthView.as_view(), name='monitoring-health'),
]
