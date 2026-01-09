from rest_framework import serializers
from boards_app.models import Boards
from django.db import models

class BoardsSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    ticket_count=serializers.IntegerField(required=False, default=0)
    tasks_to_do_count=serializers.IntegerField(required=False, default=0)
    owner_id=serializers.IntegerField(read_only=True)

    class Meta:
        model = Boards
        
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'owner_id']

    def create(self, validated_data):
        members = validated_data.get('members', [])
        validated_data['member_count'] = len(members)

        request = self.context['request']
        validated_data['owner_id'] = request.user.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'members' in validated_data:
            instance.member_count = len(validated_data['members'])
        return super().update(instance, validated_data)
    


