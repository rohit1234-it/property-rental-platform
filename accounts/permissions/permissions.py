from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only superusers."""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)


class IsBuilder(BasePermission):
    """Users whose role is 'owner'."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == "owner"
        )


class IsAdminOrBuilder(BasePermission):
    """Superusers, or users whose role is 'owner'."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_superuser or getattr(user, "role", None) == "owner")
        )