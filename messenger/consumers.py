import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Chat, Chat_User
from django.core import serializers

class MessengerConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.user.id and Chat.objects.filter(pk=self.room_name).exists():
            if Chat_User.objects.filter(chat=self.room_name, user=self.user).exists() or self.user.is_superuser:
                self.accept()

        qs = Message.objects.filter(receiver=self.room_name)
        qs_json = serializers.serialize('json', qs)
        self.send(text_data=qs_json)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        messageobj = Message(
            sender=self.user,
            receiver=Chat.objects.get(pk=self.room_name),
            text=text_data_json['message'],
            read_status=0
        )
        message = serializers.serialize('json', [messageobj, ])
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
            }
        )

        messageobj.save()

    # Receive message from room group
    def chat_message(self, event):

        # Send message to WebSocket
        self.send(text_data=event["text"])



