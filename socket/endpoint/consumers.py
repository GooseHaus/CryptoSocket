import asyncio, json, time, random
from channels.generic.websocket import AsyncWebsocketConsumer
from get_crypto_dict import get_random_dict

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
                try:
                    update_message = json.dumps(get_random_dict())
                    await self.send(update_message)
                    print("Sent update to client at", int(time.time()))
                    await asyncio.sleep(random.uniform(2, 5))
                except Exception as e:
                    print(f"Error during message send: {e}")
                    break