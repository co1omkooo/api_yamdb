from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import TitleFilter
from api.mixins import CRUDMixin
from api.permissions import (
    IsAdminOrStaff,
    IsAdminModeratorAuthorOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSafeSerializer,
    TitleSerializer,
    AuthTokenSerializer,
    SignUpSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.utils import send_confirmation_code_to_email
from reviews.models import Category, Genre, Title, Review
from users.models import User
from users.token import get_tokens_for_user


@api_view(('POST',))
@permission_classes((AllowAny,))
def signup(request):
    """Регистрация нового пользователя."""
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        user = get_object_or_404(User, username=username)
        serializer = SignUpSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data['email'] != user.email:
            return Response(
                'Почта указана неверно!', status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(raise_exception=True)
        send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if serializer.validated_data['username'] != settings.NOT_ALLOWED_USERNAME:
        serializer.save()
        send_confirmation_code_to_email(username)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        (
            f'Использование имени пользователя '
            f'{settings.NOT_ALLOWED_USERNAME} запрещено!'
        ),
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(('POST',))
@permission_classes((AllowAny,))
def get_token(request):
    """Получение токена доступа."""
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = serializer.data.get('confirmation_code')
    if confirmation_code == str(user.confirmation_code):
        return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CRUDMixin):
    """
    Вьюсет для отображения категории, ее удаления и чтения.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отображение произведени(я/ий).
    А также для их редактирования, чтения и удаления.
    """

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-year', 'name')
    permission_classes = (IsAdminOrStaff,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSafeSerializer
        return TitleSerializer


class GenreViewSet(CRUDMixin):
    """
    Вьюсет для создания, удаления жанра и отображения списка.
    """

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
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        """Получаем комментарии к конкретному отзыву."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Присваиваем автора комментарию."""
        serializer.save(author=self.request.user, review=self.get_review())


class UsersViewSet(viewsets.ModelViewSet):
    """Управление данными пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrStaff,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
