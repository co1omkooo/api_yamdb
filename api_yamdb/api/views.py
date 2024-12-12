from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import (
    IsAdminModeratorAuthorOrReadOnly,
    IsAdmin,
    IsAdminUserOrReadOnly
)
from reviews.models import Category, Genre, Title, Review, User
import random

from .serializers import (
    AuthTokenSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleSafeSerializer,
    TitleSerializer,
    UserSerializer
)


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет, разрешающий задавать GET, POST и DELETE запросы."""

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    """Регистрация нового пользователя."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    return Response(
        {
            'username': user.username,
            'email': user.email
        },
        status=status.HTTP_200_OK
    )


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    """Получение токена доступа."""
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=serializer.validated_data['username'])
    confirmation_code = serializer.validated_data.get('confirmation_code')

    if confirmation_code != str(user.confirmation_code):
        raise ValidationError(
            {'confirmation_code': ['Invalid confirmation code.']}
        )

    user.confirmation_code = None
    user.save()
    refresh = RefreshToken.for_user(user)
    tokens = {'token': str(refresh.access_token)}
    return Response(tokens, status=status.HTTP_200_OK)


def generate_confirmation_code():
    """Генерирует новый одноразовый код."""
    return random.randint(1000, 9999)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отображение произведени(я/ий).

    А также для их редактирования, чтения и удаления.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleSerializer


class CategoryViewSet(CategoryGenreViewSet):
    """Вьюсет для отображения категории, ее удаления и чтения."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Вьюсет для создания, удаления жанра и отображения списка."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet модели отзывов."""

    serializer_class = ReviewSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        """Получаем произведение для отзыва."""
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        """Получаем отзывы к конкретному произведению."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Добавляем авторизованного пользователя к отзыву."""
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset модели комментариев."""

    serializer_class = CommentSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_review(self):
        """Получаем отзыв для комментария."""
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
        )

    def get_queryset(self):
        """Получаем комментарии к конкретному отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Присваиваем автора комментарию."""
        serializer.save(author=self.request.user, review=self.get_review())


class UsersViewSet(viewsets.ModelViewSet):
    """Управление данными пользователя."""

    endpoint_user_info = settings.ENDPOINT_USER_INFO
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        url_path=endpoint_user_info,
        permission_classes=(IsAuthenticated,),
    )
    def profile(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            UserSerializer(request.user).data, status=status.HTTP_200_OK
        )
