import re

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings


def validate_year(year):
    """Проверка вводимого значения года."""
    year_now = timezone.now().year
    if year > year_now:
        raise ValidationError(
            f'Вы ввели {year} год, а сейчас {year_now} год.'
        )
    return year


def username_validator(user_name):
    forbidden_values = settings.ENDPOINT_USER_INFO
    if user_name.lower() in forbidden_values:
        raise ValidationError(f'Недопустимое имя пользователя: {user_name}')

    forbidden_chars = re.sub(r'^[\w.@+-]+\Z', '', user_name)
    if forbidden_chars:
        raise ValidationError(
            'Недопустимые символы в имени пользователя:'
            .join(set(forbidden_chars)))
    return user_name
