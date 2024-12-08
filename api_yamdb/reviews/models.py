from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import BaseTemplateClass, NameModel, BaseReviewCommentModel
from .validators import validate_year
from .constants import (
    MAX_VALUE,
    MIN_VALUE
)


class Category(BaseTemplateClass):
    """Модель категорий."""

    class Meta(BaseTemplateClass.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseTemplateClass):
    """Модель жанров."""

    class Meta(BaseTemplateClass.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    """
    Модель произведений.

    Модель, описывающий произведение, год выпуска, категорию и жанр.
    Связи модели:
        category - One to many
        genre - many to many
    """

    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=(validate_year,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Slug категории',
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class Review(BaseReviewCommentModel):
    """Модель оценки."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Произведние'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                MIN_VALUE, f'Оценка не может быть меньше {MIN_VALUE}'
            ),
            MaxValueValidator(
                MAX_VALUE, f'Оценка не может быть больше {MAX_VALUE}'
            )
        ],
        verbose_name='Оценка'
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        default_related_name = 'reviews'


class Comment(BaseReviewCommentModel):
    """
    Модель комментария.

    Модель, описыващая, комментарий и отзыв.

    Связи:
        review - one to many.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
