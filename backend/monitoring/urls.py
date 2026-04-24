from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardSummaryView, FieldUpdateListCreateView, FieldViewSet, MonitoringHealthView

router = DefaultRouter()
router.register('fields', FieldViewSet, basename='field')

urlpatterns = [
    path('health/', MonitoringHealthView.as_view(), name='monitoring-health'),
    path('dashboard/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('fields/<int:field_id>/updates/', FieldUpdateListCreateView.as_view(), name='field-updates'),
    path('', include(router.urls)),
]
