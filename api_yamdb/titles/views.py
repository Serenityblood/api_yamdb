from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from .models import *
from users.models import CustomUser
from api.serializers import (
    EmailSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [AdminPermission] # Remember!! add permision


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [GeneralPermission] # Remember!! add permision

    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer,
    permission_classes = [GeneralPermission]# Remember!! add permision

    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg(F('reviews__score'))
    )
    permission_classes = [IsAdminOrReadOnly] # Remember!! add permision
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission] # Remember!! add permision

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class ReviewCommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission] # Remember!! add permision
