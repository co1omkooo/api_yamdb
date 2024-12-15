from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение для администратора или пользователя с ролью персонала."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsAdminUserOrReadOnly(IsAdmin):
    """Разрешение только для чтения, либо полный доступ для администратора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение для автора, модератора, администратора или только чтение."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator()
            or request.user.is_admin()
        )
