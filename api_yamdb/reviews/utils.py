from django.db import models
# from django.forms import Textarea

from reviews.constants import MAX_LENGTH, CHAR_LIMIT


class NameModel(models.Model):
    """
    Родительский класс для моделей, с полем названия.
    """

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        # verbose_name_plural='Названия',
        help_text='Необходимо название категории'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:CHAR_LIMIT]


class BaseTemplateClass(NameModel):
    """
    Родительский класс для моделей Category и Genre.
    """

    slug = models.SlugField(
        verbose_name='Уникальный индентификатор',
        unique=True,

    )

    class Meta:
        abstract = True
        ordering = ('name',)
