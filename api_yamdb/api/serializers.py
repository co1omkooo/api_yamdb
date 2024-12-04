from rest_framework import serializers


from reviews.models import Review, Comment


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
        request = self.context['request']
        title = self.context['view'].kwargs['title_id']
        if request.method == 'POST':
            if Review.objects.filter(
                    author=request.user,
                    title=title
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
