import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from .models import Room, CustMessage, FreelMessage, Customer, Freelancer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_cla = self.scope['user']
        message = text_data_json['message']
        date = datetime.now()
        created_at = date.strftime("%H:%M")
        user = (user_cla.id, user_cla.first_name, user_cla.last_name)
        
        room = await self.get_or_create_room()
        
        if isinstance(user_cla, Customer):
            await database_sync_to_async(CustMessage.objects.create)(room=room, text=message, user=user_cla)
        elif isinstance(user_cla, Freelancer):
            await database_sync_to_async(FreelMessage.objects.create)(room=room, text=message, user=user_cla)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user': user,
                'created_at': created_at,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        room, _ = Room.objects.get_or_create(name=self.room_name)
        if room:
            return room
        return _