from datetime import datetime, timedelta
import jwt
from django.conf import settings


def generate_access_token(user):

    token = jwt.encode({
        'id': user.pk,
        'confirmation_code': user.confirmation_code,
        'exp': datetime.utcnow() + timedelta(days=365),
    }, settings.SECRET_KEY, algorithm='HS256')

    return token
