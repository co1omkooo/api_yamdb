from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import CONFIRMATION_LENGTH
from .constatns import MAX_LENGTH_ROLE, MAX_LENGTH


class CustomUser(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=CHOICES,
        default='user',
    )

    bio = models.TextField(
        max_length=MAX_LENGTH,
        blank=True,
    )

    email = models.EmailField(
        blank=False,
        unique=True,
    )

    confirmation_code = models.CharField(
        blank=True,
        max_length=CONFIRMATION_LENGTH,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            ),
        )

    def __str__(self):
        return self.username

    def is_user(self):
        return self.role == self.USER

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_admin(self):
        return self.role == self.ADMIN


User = get_user_model()
