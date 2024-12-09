from django.db import IntegrityError
from rest_framework import serializers

from reviews.models import Category, Title, Genre, Review, Comment, User
from reviews.constants import USERNAME_LENGTH, USER, EMAIL_LENGTH
from reviews.validators import validate_year, username_validator

from .utils import send_confirmation_code_to_email


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class TitleSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для безопасных запросов к произведениям."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для POST, PATCH и DELETE-запросов."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
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
        return TitleSafeSerializer(title).data

    def validating_year(self, year):
        return validate_year(year)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор данных модели отзывов."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        """Валидация, запрещающая создать существующий отзыв."""
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                    author=request.user,
                    title_id=self.context['view'].kwargs['title_id']
            ).exists():
                raise serializers.ValidationError('Отзыв уже существует!')
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
    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        validators=[
            username_validator,
        ],
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data.get('username'),
                email=data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Такой пользователь уже существует'
            )
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'role': USER}
        )
        user.save()

        send_confirmation_code_to_email(user)
        return user


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

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
