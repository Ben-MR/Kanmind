from rest_framework.views import APIView
from .serializers import BoardsSerializer
from boards_app.models import Boards
from rest_framework import viewsets

class BoardsListViewSet (viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer