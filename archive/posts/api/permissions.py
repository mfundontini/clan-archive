from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    message = "Only Admin or Owner Is Allowed This Permission"

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():
            if request.user.is_superuser or obj.author == request.user:
                return True
        return False
