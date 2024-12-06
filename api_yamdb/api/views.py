from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api.filters import TitleFilter
from api.mixins import CRUDMixin
from api.permissions import (
    IsAdminOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSafeSerializer,
    TitleSerializer,
)
from reviews.models import Category, Genre, Title


User = get_user_model()


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
    permission_classes = (IsAdminOrReadOnly,)
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
