from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone
from chat.models import Message, Room
from accounts.models import Profile
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("!!!!!!!!!!!!!! channels start !!!!!!!!!!!!")
        self.room_id = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_id}"
        print(f"!!!!!!!!!!!!!   chat_{self.room_id}   !!!!!!!!!!!!!!")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        current_user = self.scope["user"]
        print(current_user)

        # await sync_to_async(Profile.objects.filter(user=current_user).update)(is_online=True)

        await self.accept()
        print("accepted")

    async def disconnect(self, code):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!! disconnect !!!!!!!!!!!!!!")
        current_user = self.scope["user"]
        await sync_to_async(Profile.objects.filter(user=current_user).update)(
            is_online=False, last_seen=timezone.now())
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        current_user = self.scope["user"]
        current_room = await database_sync_to_async(Room.objects.get)(pk=self.scope["url_route"]["kwargs"]["pk"]
                                                                      )

        profile = await database_sync_to_async(lambda: current_user.profile)()

        await database_sync_to_async(Message.objects.create)(author=profile,
                                                             room=current_room, text=message)

        author_id = await database_sync_to_async(lambda: current_user.profile.pk)()
        profile_image = await database_sync_to_async(lambda: current_user.profile.image_profile)()

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                                   "message": {
                                       'text': message, 'author_id': author_id,
                                       'profile_image': profile_image.url if profile_image else None
                                   },
                                   },
        )

    async def chat_message(self, event):
        message = event["message"]['text']
        author_id = event['message']['author_id']
        profile_image = event['message']['profile_image']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {'message': message, 'author_id': author_id, 'profile_image': profile_image}))
