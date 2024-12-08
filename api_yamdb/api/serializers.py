from rest_framework import serializers

from reviews.models import Category, Title, Genre, Review, Comment
from reviews.validators import validate_year
from users.models import User

from .permissions import IsAdminOrStaff


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных запросов к произведениям."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('__all__')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для POST, PATCH и DELETE-запросов."""

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
            'id',
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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор данных модели отзывов."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', )

    def validate(self, data):
        """Валидация, запрещающая создать существующий отзыв."""
        request = self.context['request']
        title = self.context['view'].kwargs['title_id']
        if request.method == 'POST':
            if Review.objects.filter(
                    author=request.user,
                    title=title
            ).exists():
                raise serializers.ValidationError('Отзыв уже существует!')
        print(data)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор данных для модели комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class SignUpSerializer(serializers.ModelSerializer):
    """Серилизатор для входа."""

    class Meta:
        model = User
        fields = ('email', 'username')


class AuthTokenSerializer(serializers.Serializer):
    """Сериализатор токена и имени пользователя."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=16,
    )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    permission_classes = (IsAdminOrStaff,)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
