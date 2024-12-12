import asyncio, json, time, random, os, django
from channels.generic.websocket import AsyncWebsocketConsumer
from get_crypto_dict import get_random_dict
from decimal import Decimal
from asgiref.sync import sync_to_async

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoSocket.settings")
django.setup()

from endpoint.models import Coin

# MarketConsumer class is django's framework for websockets
class MarketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()
        print("New WebSocket connection established.")

    async def disconnect(self, close_code):
        # Handle disconnection
        print(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data):
        # Handle incoming messages
        data = json.loads(text_data)
        print(f"Message from client: {data}")

        # Check for a subscription event
        if data.get("event") == "subscribe" and data.get("channel") == "rates":
            # Respond to the subscription
            await self.send(json.dumps({
                "status": "subscribed",
                "channel": "rates",
            }))

            # Periodically send updates by calling script from get_crypto_dict
            while True:
                coin_data = get_random_dict()
                try:
                    update_message = json.dumps(coin_data)
                    await self.send(update_message)
                    print("Sent update to client at", int(time.time()))
                    await asyncio.sleep(random.uniform(2, 4))

                    symbol = coin_data["data"]["symbol"]
                    timestamp = coin_data["data"]["timestamp"]
                    bid = coin_data["data"]["bid"]
                    ask = coin_data["data"]["ask"]
                    spot = coin_data["data"]["spot"]
                    change = coin_data["data"]["change"]

                    # Then place/update it in the db
                    await sync_to_async(Coin.objects.update_or_create)(
                        symbol_text=symbol,
                        defaults={
                            "unix_timestamp": timestamp,
                            "bid_price": Decimal(bid),
                            "ask_price": Decimal(ask),
                            "spot_price": Decimal(spot),
                            "price_change_24hr": Decimal(change),
                        }
                    )

                except Exception as e:
                    print(f"Error during message send: {e}")
                    break