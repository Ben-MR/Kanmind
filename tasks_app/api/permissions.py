from rest_framework.permissions import BasePermission


class IsTaskOrBoardOwner(BasePermission):
    """
    Custom object-level permission.

    Grants access if the requesting user is either:
    - the owner of the bord, or
    - creator of the task

    """

    def has_object_permission(self, request, view, obj):

        user = request.user
        return (
            obj.created_by_id == user.id
                or obj.board.owner_id == user.id
        )
