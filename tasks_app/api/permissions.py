from rest_framework.permissions import BasePermission
from boards_app.models import Boards


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
    

class CanCreateTaskOnBoard(BasePermission):
    """
    Permission to control task creation based on board membership.

    This permission is evaluated on the view level (has_permission) and
    applies only to the `create` action of the TasksViewSet.

    Rules:
    - Allows task creation only if the requesting user is:
        - the owner of the referenced board, or
        - a member of the referenced board.
    - For all other actions (list, retrieve, update, destroy),
      this permission returns True and does not restrict access.

    Expected request data:
    - The request body must include a `board` field containing
      the ID of the board on which the task should be created.

    Behavior:
    - If the `board` field is missing → permission denied (403).
    - If the referenced board does not exist → permission denied (403).
      (Note: returning 404 must be handled at the view level.)
    - If the user is neither owner nor member of the board → permission denied (403).
    - If the user is owner or member → task creation is allowed.

    Notes:
    - This permission does not perform object-level checks.
    - Object-level access for existing tasks must be enforced separately
      using an object-level permission (e.g. based on `task.board`).
    """
    def has_permission(self, request, view):
        if view.action != "create":
            return True

        board_id = request.data.get("board")
        if not board_id:
            return False  

        try:
            board = Boards.objects.get(pk=board_id)
        except Boards.DoesNotExist:
            return False  

        user = request.user
        return board.owner_id == user.id or board.members.filter(id=user.id).exists()
    
