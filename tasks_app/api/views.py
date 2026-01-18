from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from boards_app.models import Boards
from .permissions import IsTaskOrBoardOwner, CanCreateTaskOnBoard
from tasks_app.models import Task, Comment
from .serializers import TasksSerializer, CommentSerializer


class TasksViewset(viewsets.ModelViewSet):
    """
    ViewSet for managing Task objects.

    Inherits from ModelViewSet and therefore provides the standard CRUD actions:
      - list
      - retrieve
      - create
      - update / partial_update
      - destroy

    Additional custom actions are defined below to filter tasks for the
    authenticated user and to handle task-related comments.
    """
        # Base queryset for all actions in this ViewSet.
    queryset = Task.objects.all()

    # Serializer used for Task objects.
    serializer_class = TasksSerializer

    permission_classes = [IsAuthenticated, CanCreateTaskOnBoard]

    #User as creator of the board
    """
    Create a new task on a specific board.

    Access rules:
    - The referenced board must exist.
    - Only the board owner or board members are allowed
      to create tasks on that board.

    Request body requirements:
    - `board`: ID of the board the task belongs to
    - other task fields as defined in the serializer

    Behavior:
    - If the board does not exist → 404 Not Found
    - If the user is not owner or member of the board → 403 Forbidden
    - If request data is invalid → 400 Bad Request
    - On success → 201 Created with serialized task data

    Notes:
    - The task creator is set automatically to the authenticated user.
    - Board ownership and membership are enforced explicitly at the view level
      instead of relying solely on DRF permissions.
    """
    def create(self, request, *args, **kwargs):
        board_id = request.data.get("board")
        board = get_object_or_404(Boards, pk=board_id)

        user = request.user
        if not (board.owner_id == user.id or board.members.filter(id=user.id).exists()):
            raise PermissionDenied("You are not allowed to create tasks on this board.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user, board=board)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
      if self.action == "destroy":
          return [IsAuthenticated(), IsTaskOrBoardOwner()]
      return [IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path="assigned-to-me")
    def assigned_to_me(self, request):
        """
        Return all tasks where the current authenticated user
        is set as the assignee.

        Endpoint:
          GET /tasks/assigned-to-me/
        """
        qs = self.get_queryset().filter(assignee=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="reviewing")
    def review_to_me(self, request):
        """
        Return all tasks where the current authenticated user
        is set as the reviewer.

        Endpoint:
          GET /tasks/reviewing/
        """
        qs = self.get_queryset().filter(reviewer=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"], url_path="comments")
    def comments(self, request, pk=None):
        """
        GET  /tasks/{id}/comments/   -> list comments for a task
        POST /tasks/{id}/comments/  -> create a comment for a task
        """
        task = self.get_object()
        board = task.board
        user = request.user

        if not (board.owner_id == user.id or board.members.filter(id=user.id).exists()):
            raise PermissionDenied("Not allowed to comment on this board.")

        if request.method == "GET":
            qs = Comment.objects.filter(task=task).order_by("-created_at")
            return Response(CommentSerializer(qs, many=True).data)

        serializer = CommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get", "delete"], url_path=r"comments/(?P<comment_id>\d+)")
    def comment_detail(self, request, pk=None, comment_id=None):
        """
        Retrieve or delete a single comment that belongs to a specific task.

        Routes:
          - GET    /tasks/{task_id}/comments/{comment_id}/
          - DELETE /tasks/{task_id}/comments/{comment_id}/

        Purpose:
          - GET returns the full serialized comment object.
          - DELETE removes the comment and returns 204 No Content.

        Safety / Access Control:
          The lookup includes both the comment ID and the task ID:
            Comment(pk=comment_id, task_id=pk)
          This guarantees that the comment must belong to the given task and
          prevents accessing or deleting comments from other tasks.

        Parameters:
          - pk: task ID (from the parent task route)
          - comment_id: comment ID (captured via the url_path regex)
        """
        comment = get_object_or_404(Comment, pk=comment_id, task_id=pk)

        if request.method == "GET":
            return Response(CommentSerializer(comment).data)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
