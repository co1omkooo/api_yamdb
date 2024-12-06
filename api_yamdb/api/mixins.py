from api.permissions import IsAdminOrReadOnly
from rest_framework import filters, mixins, viewsets


class CRUDMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет, позволяющий осуществлять GET, POST и DELETE запросы.
    Обрабатывает адреса с динамической переменной slug.
    """

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
