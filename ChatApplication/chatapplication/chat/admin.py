from django.contrib import admin
from .models import AppUser, Workspace, ChatRoom, RoomMembership, ChatMessage, MessageAttachment

admin.site.register(AppUser)
admin.site.register(Workspace)
admin.site.register(ChatRoom)
admin.site.register(RoomMembership)
admin.site.register(ChatMessage)
admin.site.register(MessageAttachment)

