from celery import shared_task
from .models import ChatSession, ChatMessage
from .services import generate_reply
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def make_assistant_reply(session_id:int, user_msg_id: int):
    session = ChatSession.objects.get(pk=session_id)
    user_msg = ChatMessage.objects.get(pk=user_msg_id)

    history = [
        {'role': m.role, 'content': m.content}
        for m in session.messages.order_by('created_at')
    ]
    assistant_txt = generate_reply(history)

    assistant = ChatMessage.objects.create(
        session=session, role='assistant', content=assistant_txt
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{session_id}",
        { 
            'type': 'assistant.message',
            'message_id': assistant.id,
            'content': assistant.content,
            'created_at': assistant.created_at.isoformat(),
        },
    )
    return assistant.id