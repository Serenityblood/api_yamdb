from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegistrationAPIView, AuthViewSet, UserAPIView

app_name = 'users'

router = DefaultRouter()
router.register(r'token', AuthViewSet, basename='token')

urlpatterns = [
    path('auth/signup/', RegistrationAPIView.as_view(), name='signup'),
    path(
        'auth/', include(router.urls)
    ),
    path('users/', UserAPIView.as_view(), name='users')
]
