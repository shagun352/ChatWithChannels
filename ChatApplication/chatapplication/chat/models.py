from django.db import models
from user.models import AppUser

class Workspace(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="chatrooms")
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workspace.name} - {self.name}"

# Tracks which users are members of which roomuseful for private rooms.
class RoomMembership(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'room')


class ChatMessage(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, null=True, blank=True, on_delete=models.CASCADE)
    recipient = models.ForeignKey(AppUser, null=True, blank=True, related_name='direct_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} at {self.created_at}"


class MessageAttachment(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
