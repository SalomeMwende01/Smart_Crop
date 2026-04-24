from django.urls import path

from .views import AuthHealthView

urlpatterns = [
    path('health/', AuthHealthView.as_view(), name='auth-health'),
]
