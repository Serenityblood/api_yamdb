from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
