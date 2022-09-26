from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, AuthSerializer
from .models import CustomUser
from .utils import generate_access_token


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthSerializer

    def post(self, request):
        if not request.data:
            raise KeyError('No data')
        username = request.data.get('username')
        confirmation_code = request.data.get(
            'confirmation_code'
        )
        user = get_object_or_404(CustomUser, username=username)
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        if confirmation_code is None:
            raise exceptions.AuthenticationFailed('Confirmation code required')
        if user.confirmation_code != confirmation_code:
            raise exceptions.AuthenticationFailed('Invalid confirmation code')
        
        access_token = generate_access_token(user)
        return Response({'Access': access_token}, status=status.HTTP_200_OK)


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