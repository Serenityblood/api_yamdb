from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_update_me, get_token, signup
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet


app_name = 'users'

router_v1_users = DefaultRouter()
router_v1_users.register(r'users', UserViewSet, basename='users')
router_v1_users.register(r'categories', CategoryViewSet)
router_v1_users.register(r'genres', GenreViewSet)
router_v1_users.register(r'titles', TitleViewSet)
router_v1_users.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router_v1_users.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='token'),
    path('users/me/', get_update_me, name='me'),
    path('', include(router_v1_users.urls)),
]
