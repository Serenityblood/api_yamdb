from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (IsAdminOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrSuperuser)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer,
                          UserSerializer, SingUpSerializer,
                          MeSerializer, TokenSerializer)
from .filter import TitlesFilter
from .mixins import CategoryGenreMixin
from .utils import sent_verification_code
from reviews.models import Review
from titles.models import Category, Genre, Title
from users.models import CustomUser


class CategoryViewSet(CategoryGenreMixin):
    """Обрабатывает запросы к categories/."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    """Обрабатывает запросы к genres/."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатвает запросы к titles/."""
    queryset = Title.objects.all().annotate(
        rating=Avg("reviews__score")
    )
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    ordering_fields = ('year',)

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает комментарии к ревью."""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к reviews/."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


@api_view(['POST'])
def signup(request):
    """Регистрация."""
    serializer = SingUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = CustomUser.objects.get_or_create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'])
    except IntegrityError as error:
        error_text = f'{error}'
        if 'username' in error_text:
            message = 'Такой юзернейм уже занят'
        if 'email' in error_text:
            message = 'Такой имейл уже занят'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        sent_verification_code(user)
        return Response(serializer.validated_data)


@api_view(['POST'])
def get_token(request):
    """Возвращает токен."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        CustomUser,
        username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'Access': f'{token}'}, status=status.HTTP_200_OK)
    return Response(
        "Отсутствует confirmation_code или он некорректен",
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    """Обрабатывает запросы к users/."""
    queryset = CustomUser.objects.all()
    lookup_field = ('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Обрабатывает запросы к users/me."""
        user = request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = MeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
