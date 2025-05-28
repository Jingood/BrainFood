from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionListSerializer,
    ChatSessionCreateSerializer,
    ChatSessionDetailSerializer,
    ChatMessageCreateSerializer,
)
from .tasks import make_assistant_reply

class SessionListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ChatSession.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return (
            ChatSessionCreateSerializer
            if self.request.method == 'POST'
            else ChatSessionListSerializer
        )
    
    def perform_create(self, serializer):
        serializer.save()


class ChatBotPageView(TemplateView):
    template_name = "chat/chat.html"


class SessionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSessionDetailSerializer
    queryset = ChatSession.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id: int):
        try:
            session = ChatSession.objects.get(pk=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({'detail': "not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChatMessageCreateSerializer(
            data=request.data, context={'session': session}
        )
        serializer.is_valid(raise_exception=True)
        user_msg: ChatMessage = serializer.save()

        make_assistant_reply.delay(session.id, user_msg.id)

        return Response(
            ChatMessageCreateSerializer(user_msg).data,
            status=status.HTTP_202_ACCEPTED
        )