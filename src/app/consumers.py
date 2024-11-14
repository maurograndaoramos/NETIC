from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
# from app.models import Message
from datetime import datetime
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['UID']
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        user = self.scope['user']

        message = text_data_json.get('message', '')

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        # Send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
            'type': 'chat_message',
            'user': user.username,
            'message': message,
            'date': ts,
            }
        )

        # message = Message(user=user, message=message)

        # message.save()


    # Receive message from chat
    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'user': event['user'],
            'message': event['message'],
            'date': event['date']
        }))