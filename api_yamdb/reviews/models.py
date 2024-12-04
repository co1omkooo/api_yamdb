from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (
    CHAR_LIMIT,
    MAX_SCORE,
    MIN_SCORE
)
from users.models import User


class Title(models.Model):
    pass


class BaseReviewCommentModel(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date')

    def __str__(self):
        return self.text[:CHAR_LIMIT]


class Review(BaseReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведние'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                MIN_SCORE, f'Оценка не может быть меньше {MIN_SCORE}'
            ),
            MaxValueValidator(
                MAX_SCORE, f'Оценка не может быть больше {MAX_SCORE}'
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
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(BaseReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
