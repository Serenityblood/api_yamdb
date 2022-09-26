from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework import serializers

from users.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя me - запрещено!')
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            '---',
            user.confirmation_code,
            'me',
            [user.email],
        )
        return user


class AuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']
