import re
from django.core import exceptions


def validate_username(value):
    if value == 'me':
        raise exceptions.ValidationError('Нельзя использовать me')
    splited = re.findall(r'.', value)
    for char in splited:
        prog = re.sub(pattern=(r'^[\w.@+-]+\Z'), repl='(1)', string=char)
        if prog != '(1)':
            raise exceptions.ValidationError(f'Символ {prog} запрещён!')
    return value
