from django.urls import re_path
from . import consumers

# Set route to required "wss://"whatever_you_want"/markets/ws"
websocket_urlpatterns = [
    re_path(r'markets/ws/$', consumers.MarketConsumer.as_asgi()),
]