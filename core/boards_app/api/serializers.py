from django.contrib.auth import get_user_model
from rest_framework import serializers
from boards_app.models import Boards
from tasks_app.models import Task
from tasks_app.api.serializers import TasksSerializer

User = get_user_model()


class BoardsListSerializer(serializers.ModelSerializer):
    """
    Serializer used for listing and creating boards.

    Provides aggregated information (member count, task counts)
    and supports assigning members on create/update.
    """

    # Expose owner id without nesting the full owner object
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    # Computed field, filled in to_representation
    member_count = serializers.IntegerField(read_only=True)

    # Aggregated task counters (computed via methods below)
    tasks_high_prio_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()

    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )
    """
    members (write_only):
    - Accepts a list of user IDs when creating or updating a board.
      Example: [1, 3, 7]
    - write_only=True means these IDs are accepted in requests,
      but not returned in the response.
    """

    class Meta:
        model = Boards
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
            "members",
        ]

    def create(self, validated_data):
        """
        Create a new board and assign members.

        Steps:
        1) Extract the 'members' list from validated_data.
        2) Create the board instance.
        3) Assign the provided members to the board.
        4) Always add the creator (request.user) as a member.

        Requirement:
        - The serializer must be instantiated with context={"request": request}.
        """
        members = validated_data.pop("members", [])
        board = Boards.objects.create(**validated_data)

        # Set selected members (overwrites existing relations)
        board.members.set(members)

        # Ensure the creator is always a member of the board
        board.members.add(self.context["request"].user.id)

        return board

    def to_representation(self, instance):
        """
        Customize the serialized output.

        Adds the computed member_count to the response.
        """
        data = super().to_representation(instance)
        data["member_count"] = instance.members.count()
        return data

    def update(self, instance, validated_data):
        """
        Update a board and optionally update its members.

        - If 'members' is provided, the member list is replaced.
        - If 'members' is not provided, the existing members remain unchanged.
        """
        member_ids = validated_data.pop("members", None)

        instance = super().update(instance, validated_data)

        if member_ids is not None:
            users = User.objects.filter(id__in=member_ids)
            instance.members.set(users)

        return instance

    def get_tasks_high_prio_count(self, board):
        """
        Return the number of tasks with HIGH priority for this board.
        """
        return Task.objects.filter(
            board=board,
            priority=Task.Priority.HIGH
        ).count()

    def get_tasks_to_do_count(self, board):
        """
        Return the number of tasks with TODO status for this board.
        """
        return Task.objects.filter(
            board=board,
            status=Task.Status.TODO
        ).count()

    def get_ticket_count(self, board):
        """
        Return the total number of tasks (tickets) for this board.
        """
        return Task.objects.filter(board=board).count()


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying board members.
    """

    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        """
        Return the user's full name if available,
        otherwise fall back to the username.
        """
        return obj.get_full_name() or obj.get_username()


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for board detail views.

    Includes:
    - Owner ID
    - Full member objects
    - All related tasks
    """

    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    tasks = TasksSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ["id", "title", "owner_id", "members", "tasks"]
