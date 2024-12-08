from api.permissions import IsAdminUserOrReadOnly
from rest_framework import filters, mixins, viewsets


class CRUDMixin(
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
