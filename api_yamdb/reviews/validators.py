import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    """Проверка вводимого значения года."""
    year_now = timezone.now().year
    if year > year_now:
        raise ValidationError({{year}: 'Привышает текущий год'})
    return year


def username_validator(user_name):
    if user_name in settings.ENDPOINT_USER_INFO:
        raise ValidationError(f'Недопустимый пользователь: {user_name}')

    forbidden_chars = re.findall(r'[^\w.@+-]', user_name)
    if forbidden_chars:
        raise ValidationError(
            'Недопустимые символы: {}.'.format(''.join(set(forbidden_chars)))
        )
    return user_name
