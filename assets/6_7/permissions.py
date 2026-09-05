from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Только автор может изменять/удалять объект"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class IsAuthenticatedForCreate(permissions.BasePermission):
    """Только авторизованные могут создавать объявления"""
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        if view.action == 'create':
            return request.user and request.user.is_authenticated
        return True