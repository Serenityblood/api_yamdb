import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from .models import CustomUser


class CustomJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=('HS256')
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missed')

        user = CustomUser.objects.filter(pk=payload['id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('No such user')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User deactivated')
        if user.confirmation_code != payload['confirmation_code']:
            raise exceptions.AuthenticationFailed(
                'Invalid confirmation code'
            )
        return (user, token)
