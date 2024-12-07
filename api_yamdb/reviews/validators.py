from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка вводимого значения года."""
    year = timezone.now().year
    if value > year:
        raise ValidationError(
            f"Вы ввели '{value}' год, а сейчас '{year}' год."
        )
    return value
