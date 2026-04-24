from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import User


class IsAdminOrAssignedAgentReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.role == User.Role.ADMIN:
            return True

        if request.user.role == User.Role.AGENT:
            if request.method in SAFE_METHODS:
                return obj.assigned_agent_id == request.user.id
            return False

        return False


class CanCreateFieldUpdate(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
