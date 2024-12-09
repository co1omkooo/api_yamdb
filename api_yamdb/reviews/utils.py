from django.db import models

from .constants import CHAR_OUTPUT_LIMIT, MAX_SLUG_LENGTH, MAX_NAME_LENGTH
from .models import User


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

    def __str__(self):
        return self.text[:CHAR_OUTPUT_LIMIT]
