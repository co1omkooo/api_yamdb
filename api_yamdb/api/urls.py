from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')

api_v1_urls = [
    path('auth/', include()),
    path('', include(v1_router.urls)),
]


urlpatterns = [
    path('v1/', include(api_v1_urls)),
]
