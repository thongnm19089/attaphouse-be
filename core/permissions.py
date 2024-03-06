from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed, AuthenticationFailed
from rest_framework.permissions import BasePermission
from apps.users.models.user import User

class UserRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not isinstance(user, User):
            return False
        if user.is_superuser:
            return True
        if user.is_block:
            raise AuthenticationFailed("USER_BLOCKED")

        return True