import re
from django.core import exceptions


def validate_username(value):
    if value == 'me':
        raise exceptions.ValidationError('Нельзя использовать me')
    prog = re.compile(r'^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$')
    if not prog.match(value):
        raise exceptions.ValidationError('Некорректный username')
    return value
