from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение, чтобы только владельцы объекта могли его редактировать.
    """

    def has_object_permission(self, request, view, instance):
        if request.method in permissions.SAFE_METHODS:
            return True

        return instance.user == request.user
