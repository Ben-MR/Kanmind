from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from tasks_app.models import Task
from .serializers import TasksSerializer, AssignedToMeSerializer
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