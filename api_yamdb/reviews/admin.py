from django.contrib import admin
from django.db import models
from django.forms import Textarea

from reviews.models import Category, Genre, Title
from reviews.utils import AdminManager


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'genre_list')
    list_display_links = ('name',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'genre')
    empty_value_display = '-пусто-'
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={'rows': 2, 'cols': 22})
        },
    }

    def genre_list(self, obj):
        return ', '.join(genre.slug for genre in obj.genre.all())
    genre_list.short_description = 'Список жанров'


@admin.register(Genre)
class GenreAdmin(AdminManager):
    ...


@admin.register(Category)
class CategoryAdmin(AdminManager):
    ...

from .models import Category, Comment, Genre, User, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админ панель отзывов."""

    list_display = (
        'title',
        'text',
        'score',
        'author',
        'pub_date'
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
        'score',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админ панель комментариев."""

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = (
        'review',
    )
    list_filter = (
        'review',
        'author',
    )
