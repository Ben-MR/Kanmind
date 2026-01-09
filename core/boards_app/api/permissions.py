from rest_framework.permissions import BasePermission, SAFE_METHODS
from boards_app.models import Boards, BoardsDetailView

class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj.owner_id ist int, obj.members ist Liste von ints (JSONField)
        uid = request.user.id
        return (obj.owner_id == uid) or (uid in (obj.members or []))
    