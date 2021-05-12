from rest_framework import permissions
from api.models import User

class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        # can write custom code
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return False

        if request.user == user:
            return True

        return False

class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        # can write custom code
        try:
            user = User.objects.get(id=request.user.id)
        except:
            return False

        if request.user == user and request.user.is_staff:
            return True

        return False