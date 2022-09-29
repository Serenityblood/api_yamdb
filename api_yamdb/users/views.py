from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view

from .permissions import IsAdminOrSuperuser
from .serializers import (
    MeSerializer, UserSerializer, SingUpSerializer,
    TokenSerializer, MeSerializer
)
from .models import CustomUser


def sent_verification_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Код: {confirmation_code}',
        '---',
        [user.email],
        fail_silently=False,
    )


@api_view(['POST'])
def signup(request):
    serializer = SingUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user, _ = CustomUser.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email'])
        sent_verification_code(user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(CustomUser, username=serializer.data['username'])
    confirmation_code = serializer.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(f'{token}', status=status.HTTP_200_OK)
    return Response(
        "Отсутствует обязательное поле или оно некорректно",
        status=status.HTTP_400_BAD_REQUEST,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    lookup_field = ('username')
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_value_regex = "[^/]+"


@api_view(['GET', 'PATCH'])
def get_update_me(request):
    if request.user.is_anonymous:
        return Response(
            "Пожалуйста авторизуйтесь",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if request.method == "GET":
        me = get_object_or_404(CustomUser, id=request.user.id)
        serializer = MeSerializer(me)
        return Response(serializer.data)
    me = get_object_or_404(CustomUser, id=request.user.id)
    serializer = MeSerializer(me, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
