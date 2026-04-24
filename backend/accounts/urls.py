from django.urls import path

from .views import AuthHealthView, LoginView, LogoutView, MeView

urlpatterns = [
    path('health/', AuthHealthView.as_view(), name='auth-health'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
]
