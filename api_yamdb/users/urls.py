from django.urls import path

from .views import RegistrationAPIView

app_name = 'users'

urlpatterns = [
    path('auth/signup/', RegistrationAPIView.as_view()),
]
