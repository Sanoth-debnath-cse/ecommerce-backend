from rest_framework.permissions import BasePermission


class IsShopOwner(BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and request.user.is_superuser
            and request.user.is_staff
        ):
            return True
        return False
