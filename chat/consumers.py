import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['user'].username if self.scope['user'].is_authenticated else None
        self.other_username = self.scope['url_route']['kwargs'].get('username')

        if not self.me or self.me == self.other_username:
            await self.close()
            return

        # 1:1 xonani yaratamiz
        self.room_group_name = self.get_room_name(self.me, self.other_username)

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
        data = json.loads(text_data)
        message = data.get("message", "")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{self.me}: {message}",
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))

    def get_room_name(self, user1, user2):
        # 2 foydalanuvchini tartiblab bir xonaga joylaymiz
        return "_".join(sorted([user1, user2]))
