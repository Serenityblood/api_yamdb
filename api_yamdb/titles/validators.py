import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if 0 > value > datetime.datetime.now().year:
        raise ValidationError(
            'Год выпуска не может быть больше нынешнего или 0'
        )
    return value
