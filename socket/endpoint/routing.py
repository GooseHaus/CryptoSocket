from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'markets/ws/$', consumers.MarketConsumer.as_asgi()),
]