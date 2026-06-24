from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from chat.models import Message, Room
from accounts.models import Profile
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["pk"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        current_user = self.scope["user"]
        Profile.objects.filter(user=current_user).update(is_online=True)

        self.accept()

    def disconnect(self, code):
        current_user = self.scope["user"]
        Profile.objects.filter(user=current_user).update(
            is_online=False, last_seen=timezone.now())
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        current_user = self.scope["user"]
        current_room = Room.objects.get(pk=self.scope["url_route"]["kwargs"]["pk"]
                                        )

        Message.objects.create(author=current_user.profile,
                               room=current_room, text=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({'message': message}))
