from rest_framework import serializers

from reviews.models import Category, Title, Genre
from reviews.validators import validate_year


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанров.
    """

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий.
    """

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSafeSerializer(serializers.ModelSerializer):
    """
    Класс-сериализатор для безопасных запросов.
    """

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений для POST, PATCH и DELETE-запросов.
    """

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

    def readable_serializer(self, title):
        """Определяет сериализатор для чтения."""
        serializer = TitleSafeSerializer(title)
        return serializer.data

    def validating_year(self, value):
        return validate_year(value)
