from rest_framework import permissions


SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}
FIND_ALLOWED_METHODS_OF_REVIEW = {'POST', 'PUT', 'DELETE'}


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


