from rest_framework.views import APIView
from .serializers import BoardsSerializer, BoardDetailSerializer
from boards_app.models import Boards
from rest_framework import viewsets
from .permissions import IsOwnerOrMember
from rest_framework.permissions import IsAuthenticated

class BoardsListViewSet (viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember] 
    
    def get_queryset(self):
        qs = Boards.objects.all()
        uid = self.request.user.id

        if self.action == "list":
            allowed_ids = [
                b.id for b in qs
                if b.owner_id == uid or uid in (b.members or [])
            ]
            return qs.filter(id__in=allowed_ids)

        return qs

    def get_serializer_class(self):
        if self.action in ("retrieve"):
            return BoardDetailSerializer

        return BoardsSerializer
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsAuthenticated()]
    #     return [IsAuthenticated(), IsOwnerOrMember()]