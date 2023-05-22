from rest_framework import permissions

from users.models import UserRole


class IsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.role == UserRole.ADMIN):
            return True


class IsAdminOrModeratorOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.role == UserRole.ADMIN
                or request.user.role == UserRole.MODERATOR)
