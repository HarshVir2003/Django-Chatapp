import json
import base64
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # Encode the message to bytes using the correct encoding
        encoded_message = message.encode('utf-8')
        # Base64 encode the message
        encoded_message_base64 = base64.b64encode(encoded_message).decode('utf-8')
        # Send message to room group
        print(encoded_message_base64)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": encoded_message_base64}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Decode the base64 encoded message
        decoded_message_base64 = base64.b64decode(message)
        # Decode the bytes to UTF-8 string
        decoded_message = decoded_message_base64.decode('utf-8')

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": decoded_message}))
