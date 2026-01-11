from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from tasks_app.models import Task
from .serializers import TasksSerializer, CommentSerializer
from rest_framework.response import Response


class TasksViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all() 
    serializer_class = TasksSerializer

    @action(detail=False, methods=["get"], url_path='assigned-to-me')
    def assigned_to_me(self, request):
        qs = self.get_queryset().filter(assignee=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"], url_path='reviewing')
    def review_to_me(self, request):
        qs = self.get_queryset().filter(reviewer=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"], url_path='comments')
    def comments(self, request, pk=None):
        return Response('serializer.data')
    
    @action(detail=True, methods=["post"], url_path="comments")
    def comments(self, request, pk=None):
        task = self.get_object()
        serializer = CommentSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task)  
        return Response(serializer.data)