from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings

from .constants import (
    MAX_SCORE,
    MIN_SCORE,
    ROLE_CHOICES,
    ADMIN,
    USER,
    MODERATOR,
    USERNAME_LENGTH,
    MAX_NAME_LENGTH,
    EMAIL_LENGTH,
    CHAR_OUTPUT_LIMIT,
    MAX_SLUG_LENGTH
)
# from .utils import NameSlugModel, TextAuthorDateModel
from .validators import validate_year, username_validator


class User(AbstractUser):
    """Модель пользователя."""
    confirmation_length = settings.CONFIRMATION_LENGTH

    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль',
    )

    bio = models.TextField(
        blank=True,
        verbose_name='Описание',
    )

    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        blank=False,
        unique=True,
        verbose_name='Электронная почта'
    )

    username = models.CharField(
        max_length=USERNAME_LENGTH,
        unique=True,
        validators=[username_validator]
    )

    confirmation_code = models.CharField(
        blank=True,
        max_length=confirmation_length,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
        # constraints = (
        #     models.UniqueConstraint(
        #         fields=('username', 'email'),
        #         name='unique_username_email'
        #     ),
        # )

    def __str__(self):
        return self.username

    def is_user(self):
        return self.role == USER

    def is_moderator(self):
        return self.role == MODERATOR

    def is_admin(self):
        return self.role == ADMIN or self.is_staff


class NameSlugModel(models.Model):
    """Абстрактная модель для категории и жанра."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        verbose_name='Идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)
        verbose_name = 'Наименование'
        verbose_name_plural = 'Наименования'

    def __str__(self):
        return self.name[:CHAR_OUTPUT_LIMIT]


class Category(NameSlugModel):
    """Модель категорий."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugModel):
    """Модель жанров."""

    class Meta(NameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Наименование произведения'
    )

    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория произведения',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class TextAuthorDateModel(models.Model):
    """Абстрактная модель для отцывов и комментариев"""

    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(TextAuthorDateModel):
    """Модель оценки."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Произведние'
    )
    score = models.IntegerField(
        validators=(
            MinValueValidator(
                MIN_SCORE, f'Оценка не может быть меньше {MIN_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE, f'Оценка не может быть больше {MAX_SCORE}'
            )
        ),
        verbose_name='Оценка'
    )

    class Meta(TextAuthorDateModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            ),
        )
        default_related_name = 'reviews'


class Comment(TextAuthorDateModel):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(TextAuthorDateModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
