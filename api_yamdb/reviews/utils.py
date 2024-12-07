from django.contrib import admin
from django.db import models
from django.forms import Textarea

from api_yamdb.api_yamdb.settings import MAX_SLICE
from reviews.constants import MAX_LENGTH


class AdminManager(admin.ModelAdmin):
    list_display = ('pk', 'name')
    search_fields = ('name',)
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 2, 'cols': 22}),
        },
    }

    class Meta:
        abstract = True


class NameModel(models.Model):
    """
    Родительский класс для моделей, с полем названия.
    """

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        verbose_name_plural='Названия',
        help_text='Необходимо название категории'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:MAX_SLICE]


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
