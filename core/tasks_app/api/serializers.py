from django.contrib.auth import get_user_model
from rest_framework import serializers
from tasks_app.models import Task 
from boards_app.models import Boards


User = get_user_model()

class AssigneeSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return obj.get_full_name() or obj.get_username()

class TasksSerializer(serializers.ModelSerializer):
    assignee = AssigneeSerializer(read_only=True)
    reviewer = AssigneeSerializer(read_only=True)    
    
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
            "id", "board", "title", "description", "status", "priority",
            "assignee", 'assignee_id', "reviewer", 'reviewer_id', "due_date", "comments_count",
        ]

    def create(self, validated_data):
        validated_data.setdefault("assignee", self.context["request"].user)
        return super().create(validated_data)
    


    # def create(self, validated_data):
    #     board_id = validated_data.pop("tasks", [])
    #     board = Task.objects.create(**validated_data)

    #     if board_id:
    #         users = User.objects.filter(id__in=board_id)
    #         board.tasks.set(users)

    #     return board

class AssignedToMeSerializer(serializers.ModelSerializer):
    pass