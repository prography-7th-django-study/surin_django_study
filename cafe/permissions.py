from rest_framework import permissions


SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}


class IsAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, views, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

