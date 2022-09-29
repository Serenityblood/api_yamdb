from xml.etree.ElementInclude import include
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_update_me, get_token, signup

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
    path('users/me/', get_update_me, name='me'),
    path('', include(router.urls)),
]
