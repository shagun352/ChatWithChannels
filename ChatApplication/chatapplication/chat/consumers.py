from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

from chat.models import ChatMessage, ChatRoom
from user.models import AppUser  # your custom user model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Mark user as online
        await self.set_user_online()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Notify others user is online
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user': self.scope['user'].username,
                'status': 'online',
            }
        )

    async def disconnect(self, close_code):
        # Mark user as offline
        await self.set_user_offline()

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify others user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_status',
                'user': self.scope['user'].username,
                'status': 'offline',
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        sender = await self.get_user(self.scope['user'])
        room = await self.get_room(self.room_name)

        if sender and room and message:
            # Save message to DB
            chat_message = await self.save_message(sender, room, None, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': sender.username,
                    'timestamp': chat_message.created_at.isoformat(),
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket clients
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    async def user_status(self, event):
        # Send user status updates to WebSocket clients
        await self.send(text_data=json.dumps({
            'user': event['user'],
            'status': event['status'],
        }))

    @database_sync_to_async
    def get_user(self, user_lazy_obj):
      
        return AppUser.objects.get(pk=2)
        

    @database_sync_to_async
    def get_room(self, room_name):
        try:
            return ChatRoom.objects.get(name=room_name)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, room, recipient, content):
        return ChatMessage.objects.create(
            sender=sender,
            room=room,
            recipient=recipient,
            content=content
        )

    @database_sync_to_async
    def set_user_online(self):
        user = AppUser.objects.get(pk=2)
        user.is_online = True
        user.save()

    @database_sync_to_async
    def set_user_offline(self):
        user = AppUser.objects.get(pk=2)
        user.is_online = False
        user.save()
