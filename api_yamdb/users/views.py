from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, mixins, viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import AdminOnlyPermission
from .serializers import RegistrationSerializer, AuthSerializer, UserSerializer
from .models import CustomUser
from .utils import generate_access_token


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        email = request.data.get('email')
        existing_user = CustomUser.objects.filter(email=email).first()
        if existing_user:
            send_mail(
                '---',
                existing_user.confirmation_code,
                'me',
                [existing_user.email],)
            return Response(
                {'message': 'Код подтверждения на почте'},
                status=status.HTTP_200_OK)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('username'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        confirmation_code = request.data.get(
            'confirmation_code'
        )
        user = get_object_or_404(CustomUser, username=username)
        if confirmation_code is None:
            raise exceptions.AuthenticationFailed('Confirmation code required')
        if user.confirmation_code != confirmation_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        access_token = generate_access_token(user)
        return Response({'Access': access_token}, status=status.HTTP_200_OK)


class UserAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = ('username',)
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
