import re
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Нельзя использовать "me" в качестве имени'
            'пользователя')
    if re.search(r'^[\w@\.\+\-]+$', value) is None:
        raise ValidationError(
            f'В username недопустимый символ {value}'
        )


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )
