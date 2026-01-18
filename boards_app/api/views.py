from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from boards_app.models import Boards
from .serializers import BoardUpdateSerializer, BoardsListSerializer, BoardDetailSerializer
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
    permission_classes = [IsAuthenticated, IsOwnerOrMember]

    serializer_list_class = BoardsListSerializer
    serializer_detail_class = BoardDetailSerializer
    serializer_create_class = BoardsListSerializer
    serializer_update_class = BoardUpdateSerializer

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
        Return the appropriate serializer class depending on the current action.

        Serializer selection logic:

        - list:
            Returns BoardsListSerializer.
            Used for listing all boards accessible to the user.

        - create:
            Returns BoardsListSerializer.
            Used for creating a new board. Accepts member IDs and returns
            aggregated board information.

        - retrieve:
            Returns BoardDetailSerializer.
            Used for fetching a single board with full detail information,
            including members and tasks.

        - update / partial_update:
            Returns BoardUpdateSerializer.
            Used for updating an existing board.
            The response structure differs from GET and includes:
            - owner_data (full owner object)
            - members_data (full member objects)

        This approach allows different response structures per action
        while keeping request validation and serialization logic clean
        and explicit.
        """
        if self.action == "create":
            return self.serializer_create_class
        if self.action == "retrieve":
            return self.serializer_detail_class
        if self.action == "list":
            return self.serializer_list_class
        if self.action in ["update", "partial_update"]:
            return self.serializer_update_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        """
        Create a new board and assign the current user as the owner.

        The owner is taken from the authenticated request user and
        is not expected to be provided by the client.
        """
        serializer.save(owner=self.request.user)
