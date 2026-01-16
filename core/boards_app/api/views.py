from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import Boards
from .serializers import BoardsListSerializer, BoardDetailSerializer
from .permissions import IsOwnerOrMember


class BoardsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing boards.

    Features:
    - Only authenticated users can access this endpoint.
    - Users can only see boards they own or are members of.
    - Object-level access is additionally protected by IsOwnerOrMember.
    - Uses different serializers for list/create vs. retrieve actions.
    """

    queryset = Boards.objects.all()
    serializer_class = BoardsListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    def get_queryset(self):
        """
        Return only boards the current user is allowed to access.

        A board is included if:
        - the user is the owner of the board, OR
        - the user is listed as a member of the board

        The `distinct()` call prevents duplicate results when both
        conditions match.
        """
        user = self.request.user
        return Boards.objects.filter(
            Q(owner=user) | Q(members=user)
        ).distinct()

    def get_serializer_class(self):
        """
        Select the serializer class based on the current action.

        - retrieve → BoardDetailSerializer (includes members and tasks)
        - all other actions → BoardsListSerializer (list/create/update)
        """
        if self.action == "retrieve":
            return BoardDetailSerializer
        return BoardsListSerializer

    def perform_create(self, serializer):
        """
        Create a new board and assign the current user as the owner.

        The owner is taken from the authenticated request user and
        is not expected to be provided by the client.
        """
        serializer.save(owner=self.request.user)
