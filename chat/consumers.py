from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatSession, ChatMessage
from .serializers import ChatMessageCreateSerializer
from .tasks import make_assistant_reply

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        user = self.scope['user']
        exists = await database_sync_to_async(
            ChatSession.objects.filter(id=self.session_id, user=user).exist
        )()
        if not exists:
            await self.close()
            return
        
        await self.channel_layer.group_add(f"chat_{self.session_id}", self.channel_name)
        await self.accept()
    
    async def receive_json(self, content, **kwargs):
        if content.get('type') != 'user_message':
            return
        user_text = content.get('text', '').strip()
        if not user_text:
            return
        
        serializer = ChatMessageCreateSerializer(
            data={'content': user_text},
            context={'session_id': self.session_id, 'session': None},
        )
        if not serializer.is_valid():
            return
        msg_obj = await database_sync_to_async(serializer.save)()

        make_assistant_reply.delay(self.session_id, msg_obj.id)

    async def assistant_message(self, event):
        await self.send_json(
            {
                'type': 'assistant_message',
                'message_id': event['message_id'],
                'content': event['content'],
                'created_at': event['cerated_at'],
            }
        )
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(f"chat_{self.session_id}", self.channel_name)
