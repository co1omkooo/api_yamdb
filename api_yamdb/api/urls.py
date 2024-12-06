from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UsersViewSet, get_token, signup

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', signup, name='user-registration'),
    path('v1/auth/token/', get_token, name='user_get_token'),
    path('v1/', include(router.urls)),
]
