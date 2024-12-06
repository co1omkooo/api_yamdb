from django.db import models

from .utils import BaseTemplateClass, NameModel
from .validators import validate_year


class Category(BaseTemplateClass):
    """
    Класс категорий.
    """

    class Meta(BaseTemplateClass.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseTemplateClass):
    """
    Класс жанров.
    """

    class Meta(BaseTemplateClass.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(NameModel):
    """
    Класс произведений.

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
