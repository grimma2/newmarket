from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import BaseUser, Chat, Message

import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.chat_pk = self.scope['url_route']['kwargs']['chat_pk']
        self.user = BaseUser.objects.get(username=self.scope['url_route']['kwargs']['username'])
        self.chat_name = f'chat_{self.chat_pk}'
        self.chat = Chat.objects.get(pk=self.chat_pk)

        self.valid_user()

        async_to_sync(self.channel_layer.group_add)(
            self.chat_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        Message.objects.create(
            user=BaseUser.objects.get(username=username),
            chat=self.chat,
            text=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'event': 'Send',
            'message': message,
            'username': username
        }))

    def valid_user(self):
        if not self.user.username in [user.username for user in self.chat.users.all()]:
            raise Exception('User try open private chat')
