"""
ASGI config for demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
#
# application = get_asgi_application()


# videocall/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path, path
from channels.sessions import SessionMiddlewareStack

import call.routing
from call.consumer import CallConsumer
from sockets.consumers import AsyncVoiceConsumer, VoiceConsumer, SpeechToTextConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

django_application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        path('ws/call/', CallConsumer.as_asgi()),
                        path('ws/asyncSocket/', AsyncVoiceConsumer.as_asgi()),
                        path('ws/syncSocket/', VoiceConsumer.as_asgi()),
                        path('ws/stt/', SpeechToTextConsumer.as_asgi()),

                    ]
                )
            )
        )
    ),
})

