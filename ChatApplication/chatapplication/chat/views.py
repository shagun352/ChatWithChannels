from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Workspace, ChatRoom, RoomMembership, ChatMessage, MessageAttachment
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

class WorkspaceListCreateView(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        workspace_id = self.request.data.get("workspace")
        workspace = get_object_or_404(Workspace, id=workspace_id)
        serializer.save(workspace=workspace)

class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs.get("room_id")
        return ChatMessage.objects.filter(room_id=room_id).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
