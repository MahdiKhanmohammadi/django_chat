from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from chat.models import Message, Room
from accounts.models import Profile


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        current_user = self.scope["user"]
        Profile.objects.filter(user=current_user).update(is_online=True)

        self.accept()

    def disconnect(self, code):
        current_user = self.scope["user"]
        Profile.objects.filter(user=current_user).update(
            is_online=False, last_seen=timezone.now())

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        current_user = self.scope["user"]
        current_room = Room.objects.get(pk=self.scope["url_route"]["kwargs"]["pk"]
                                        )

        Message.objects.create(author=current_user.profile,
                               room=current_room, text=message)
        self.send(text_data=json.dumps({'message': message}))
