from rest_framework import permissions

class IsCoordinator(permissions.BasePermission):
    """
    Allows access only to users with is_coordinator=True
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_coordinator', False))
