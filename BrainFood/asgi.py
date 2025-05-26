"""
ASGI config for BrainFood project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BrainFood.settings')

django_asgi = get_asgi_application()

import chat.routing

application = ProtocolTypeRouter({
    'http': django_asgi,
    'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websoket_urlpatterns)),
})
