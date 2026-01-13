from django.contrib.auth import get_user_model
from rest_framework import serializers
from boards_app.models import Boards
from tasks_app.models import Task
from tasks_app.api.serializers import TasksSerializer


User = get_user_model()


class BoardsListSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
   
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Boards
        fields = [
            "id", "title", "member_count",
            "ticket_count", "tasks_to_do_count", "tasks_high_prio_count",
            "owner_id", "members"
        ]

    def create(self, validated_data):
        members = validated_data.pop("members", [])
        board = Boards.objects.create(**validated_data)
        board.members.set(members)   
        return board

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["member_count"] = instance.members.count()
        return data

    def update(self, instance, validated_data):
        member_ids = validated_data.pop("members", None)

        instance = super().update(instance, validated_data)

        if member_ids is not None:
            users = User.objects.filter(id__in=member_ids)
            instance.members.set(users)

        return instance 
    
    def get_tasks_high_prio_count(self, board):
        return Task.objects.filter(
            board=board,
            priority=Task.Priority.HIGH
        ).count()
    
    def get_tasks_to_do_count(self, board):
        return Task.objects.filter(
            board=board,
            status=Task.Status.TODO
        ).count()
    
    def get_ticket_count(self, board):
        return Task.objects.filter(
            board=board,
        ).count()


    
class MemberSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

    def get_fullname(self, obj):
        return obj.get_full_name() or obj.get_username()


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    tasks = TasksSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ["id", "title", "owner_id", "members", 'tasks']
