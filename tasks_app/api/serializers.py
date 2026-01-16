from django.contrib.auth import get_user_model
from rest_framework import serializers
from tasks_app.models import Task, Comment

# Use the configured Django user model (supports custom User models).
User = get_user_model()


class AssigneeSerializer(serializers.ModelSerializer):
    """
    Lightweight nested serializer for representing users assigned to a task
    (or reviewing a task).

    Exposes:
      - id: primary key of the user
      - email: user's email address
      - fullname: computed display name (full name preferred, username fallback)
    """

    # Computed field populated via get_fullname().
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        """
        Return a human-friendly display name.

        Priority:
          1) Django's full name (first_name + last_name) if available
          2) Username as a fallback
        """
        return obj.get_full_name() or obj.get_username()


class TasksSerializer(serializers.ModelSerializer):
    """
    Serializer for Task objects.

    Read side:
      - assignee / reviewer are nested user objects (read-only) using AssigneeSerializer.
      - comments_count is a computed integer field.

    Write side:
      - assignee_id / reviewer_id accept user primary keys and map them to the
        Task.assignee / Task.reviewer relations via `source=...`.
      - assignee defaults to the current request user during creation if not provided.
    """

    # Nested user representations for responses (read-only).
    assignee = AssigneeSerializer(read_only=True)
    reviewer = AssigneeSerializer(read_only=True)

    # Computed field: number of comments on the task.
    comments_count = serializers.SerializerMethodField()

    # Write-only fields that accept user IDs and populate FK relations via `source`.
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        write_only=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "assignee_id",
            "reviewer",
            "reviewer_id",
            "due_date",
            "comments_count",
        ]

    def create(self, validated_data):
        """
        Create a Task instance.

        If no assignee was provided via assignee_id, default to the authenticated
        request user.
        """
        validated_data.setdefault("assignee", self.context["request"].user)
        return super().create(validated_data)

    def get_comments_count(self, task):
        """
        Return the number of Comment rows linked to this task.

        Note: This performs a query per serialized task. For list endpoints,
        consider annotating the queryset with Count('comment') to avoid N+1 queries.
        """
        return Comment.objects.filter(task=task).count()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment objects.

    - author is returned as a display string (full name preferred, username fallback).
    - author is set automatically to the authenticated request user on create.
    """

    # Expose author as a computed string rather than a nested user object.
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", "content"]

    def get_author(self, obj):
        """
        Return the author's display name.

        Priority:
          1) Django's full name (first_name + last_name) if available
          2) Username as a fallback
        """
        user = obj.author
        return user.get_full_name() or user.get_username()

    def create(self, validated_data): 
        """
        Create a Comment instance and set its author to the authenticated request user.
        """
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
