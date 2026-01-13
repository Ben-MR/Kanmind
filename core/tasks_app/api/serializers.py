from django.contrib.auth import get_user_model
from rest_framework import serializers
from tasks_app.models import Task, Comment


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
    comments_count = serializers.SerializerMethodField()
    
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
    
    def get_comments_count_count(self, task):
        return Comment.objects.filter(task=task).count()
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ["id", "created_at", "author", 'content']

    def get_author(self, obj):
        user = obj.author
        return user.get_full_name() or user.get_username()
    
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)