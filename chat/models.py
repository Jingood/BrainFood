import uuid
from django.conf import settings
from django.db import models

class ChatSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_session',
    )
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
    
    def __str__(self):
        return f"[{self.id}] {self.title or 'untitled'}"
    
class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'user'
        ASSITANT = 'assistant', 'assistant'
        SYSTEM = 'system', 'system'
    
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    role = models.CharField(max_length=9, choices=Role.choices)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [
            models.Index(fields=('session', 'created_at')),
        ]
    
    def __str__(self):
        return f"{self.session_id}-{self.role}: {self.content[:30]}..." 


