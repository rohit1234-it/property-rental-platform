from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.user_type.user_type.lower() == 'admin'))
        
class IsBuilder(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and (request.user.user_type.user_type.lower() == 'builder'))

class IsAdminOrBuilder(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and (request.user.is_superuser or request.user.user_type.user_type.lower() == 'admin' or request.user.user_type.user_type.lower() == 'builder'))