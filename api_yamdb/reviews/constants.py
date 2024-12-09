MIN_SCORE = 1  # Минимальное значение.

MAX_SCORE = 10  # Максимальное значение.

CHAR_OUTPUT_LIMIT = 20  # Максимальная длина комментария.

MAX_NAME_LENGTH = 256

MAX_SLUG_LENGTH = 50

EMAIL_LENGTH = 254

USERNAME_LENGTH = 150

USER = 'user'

MODERATOR = 'moderator'

ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),
)
