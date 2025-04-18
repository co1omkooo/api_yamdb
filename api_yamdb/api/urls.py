from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UsersViewSet, get_token, signup
from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    CommentViewSet,
    ReviewViewSet,
)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='title')
v1_router.register('categories', CategoryViewSet, basename='category')
v1_router.register('genres', GenreViewSet, basename='genre')
v1_router.register('users', UsersViewSet, basename='users')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_url = [
    path('signup/', signup, name='user-registration'),
    path('token/', get_token, name='user_get_token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_url)),
]
