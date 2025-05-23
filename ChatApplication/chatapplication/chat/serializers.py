from rest_framework import serializers
from .models import Workspace, ChatRoom, RoomMembership, ChatMessage, MessageAttachment
from user.models import AppUser

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class RoomMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMembership
        fields = '__all__'

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'room', 'recipient', 'content', 'created_at', 'is_read', 'attachments']
