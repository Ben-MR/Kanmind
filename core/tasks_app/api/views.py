from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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

        if request.method == "GET":
            qs = Comment.objects.filter(task=task).order_by("-created_at")
            return Response(CommentSerializer(qs, many=True).data)

        serializer = CommentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path=r"comments/(?P<comment_id>\d+)")
    def comment_detail(self, request, pk=None, comment_id=None):
        """
        Retrieve a single comment belonging to a specific task.

        Endpoint:
          GET /tasks/{id}/comments/{comment_id}/

        Safety:
          The lookup ensures that the comment belongs to the given task,
          preventing access to comments of other tasks.
        """
        comment = get_object_or_404(Comment, pk=comment_id, task_id=pk)
        return Response(CommentSerializer(comment).data)
