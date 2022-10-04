from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Пермишен для админа или только на чтение."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Пермишен для админа или автора."""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdminOrSuperuser(permissions.BasePermission):
    """Пермишен для админа."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)
