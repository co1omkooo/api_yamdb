from django.db import models

from reviews.constants import MAX_LENGTH, CHAR_LIMIT
from users.models import User


class NameModel(models.Model):
    """Родительский класс для моделей, с полем названия."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        help_text='Необходимо название категории'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:CHAR_LIMIT]


class BaseTemplateClass(NameModel):
    """Родительский класс для моделей Category и Genre."""

    slug = models.SlugField(
        verbose_name='Уникальный индентификатор',
        unique=True,

    )

    class Meta:
        abstract = True
        ordering = ('name',)


class BaseReviewCommentModel(models.Model):
    """
    Модель отзывов.

    Модель, описывающая отзыв, автора и его дату.
    Связи модели:
        author - one to many.
    """

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
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:CHAR_LIMIT]
