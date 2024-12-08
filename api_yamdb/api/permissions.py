from rest_framework import permissions


class IsAdminOrStaff(permissions.BasePermission):
    """Разрешение для администратора или пользователя с ролью персонала."""

    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or (request.user.is_authenticated and request.user.is_admin())
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Разрешение только для чтения, либо полный доступ для администратора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin())
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
