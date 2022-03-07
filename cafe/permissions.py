from rest_framework import permissions


SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_staff)

