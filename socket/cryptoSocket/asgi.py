"""
ASGI config for cryptoSocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import endpoint.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoSocket.settings')

# Allow routing of websockets
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            endpoint.routing.websocket_urlpatterns
        )
    )
})
