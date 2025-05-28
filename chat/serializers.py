from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'role', 'content', 'created_at')
        read_only_fields = ('id', 'created_at', 'role')

class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'created_at', 'last_message')
    
    def get_last_message(self, obj: ChatSession):
        msg = obj.message.order_by('-created_at').first()
        return msg.content[:50] if msg else ""

class ChatSessionDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'created_at', 'messages')

class ChatSessionCreateSerializer(serializers.ModelSerializer):
    first_message = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'first_message')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        user = self.context['request'].user
        first_text = validated_data.pop('first_message', '').strip()

        session = ChatSession.objects.create(user=user, **validated_data)

        if first_text:
            ChatMessage.objects.create(
                session=session,
                role=ChatMessage.Role.USER,
                content=first_text
            )
        return session

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'content')
        read_only_fields = ('id',)

    def create(self, validated_data):
        session: ChatSession = self.context['session']
        return ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.USER,
            **validated_data,
        )