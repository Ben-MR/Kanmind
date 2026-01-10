from rest_framework.permissions import BasePermission

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        u = request.user
        return obj.owner_id == u.id or obj.members.filter(id=u.id).exists()
    