from rest_framework import serializers
from django.contrib.auth.models import User
from boards_app.models import Boards, BoardsDetailView
from django.db import models

class BoardsSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    ticket_count=serializers.IntegerField(required=False, default=0)
    tasks_to_do_count=serializers.IntegerField(required=False, default=0)
    owner_id=serializers.IntegerField(read_only=True)
    members = serializers.JSONField(write_only=True)

    class Meta:
        model = Boards        
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'owner_id', 'members']

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["owner_id"] = request.user.id

        members = validated_data.get("members") or []
        validated_data["member_count"] = len(members)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # nach Update: member_count aus dem gespeicherten Wert berechnen
        instance.member_count = len(instance.members or [])
        instance.save(update_fields=["member_count"])

        return instance
    
class BoardDetailSerializer (serializers.ModelSerializer):
    # tasks = models.JSONField(default=list, blank=True)
    members = serializers.SerializerMethodField()
    
    class Meta:
        model = BoardsDetailView        
        fields = ['id', 'title', 'owner_id', 'members']

    def get_members(self, obj):
        return [
            {
                "id": u.id,
                "fullname": u.get_full_name(),
                "email": u.email,
            }
            for u in User.objects.filter(id__in=obj.members)
        ]

