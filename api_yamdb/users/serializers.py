from django.conf import settings
from rest_framework import serializers

from users.models import CustomUser
from .validators import validate_username


class ValidateUsername(serializers.Serializer):

    def validate_username(self, value):
        return validate_username(value)


class UserSerializer(serializers.ModelSerializer, ValidateUsername):

    class Meta:
        model = CustomUser
        lookup_fields = ('username')
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
            'email',
        )


class SingUpSerializer(ValidateUsername):
    username = serializers.CharField(max_length=settings.USERNAME_SIZE)
    email = serializers.EmailField(max_length=settings.EMAIL_SIZE)


class TokenSerializer(ValidateUsername):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=500)


class MeSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',)
        model = CustomUser
