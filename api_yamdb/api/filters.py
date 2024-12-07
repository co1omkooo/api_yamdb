from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """
    Фильтр произведений по полям.
    """

    name = CharFilter(
        field_name='name',
        lookup_expr='contains',
    )
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains',
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains',
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
