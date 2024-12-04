from rest_framework import permissions


class IsAdminOrStaffPermission(permissions.BasePermission):
    pass


class IsAuthorOrModerPermission(permissions.BasePermission):
    pass


class IsAdminOrReadOnly(permissions.BasePermission):
    pass
