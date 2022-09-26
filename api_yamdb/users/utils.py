from datetime import datetime, timedelta
import jwt
from django.conf import settings


def generate_access_token(user):

    token = jwt.encode({
        'username': user.username,
        'id': user.pk,
        'confirmation_code': user.confirmation_code,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(days=365),
    }, settings.SECRET_KEY, algorithm='HS256')

    return token
