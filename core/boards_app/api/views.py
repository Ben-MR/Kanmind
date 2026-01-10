from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import Boards
from .serializers import BoardsListSerializer, BoardDetailSerializer
from .permissions import IsOwnerOrMember

class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all() 
    serializer_class = BoardsListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get_queryset(self):
        u = self.request.user
        return Boards.objects.filter(Q(owner=u) | Q(members=u)).distinct()
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return BoardDetailSerializer
        return BoardsListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
