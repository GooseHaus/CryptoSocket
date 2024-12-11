import asyncio, websockets, json, ssl, os, django
from decimal import Decimal
from asgiref.sync import sync_to_async

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoSocket.settings")
django.setup()

from endpoint.models import Coin

# Disabled cert verification (local use and testing)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Connect to websocket, subscribe the events stream, print responses
async def connect_to_websocket():
    uri = "wss://localhost:8000/markets/ws/"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        await websocket.send(json.dumps({"event": "subscribe", "channel": "rates"}))
        while True:
            response = await websocket.recv()
            print("Response from server:", response)

            # Pull data from the websocket's json
            data = json.loads(response)
            if "data" in data:
                symbol = data["data"]["symbol"]
                timestamp = data["data"]["timestamp"]
                bid = data["data"]["bid"]
                ask = data["data"]["ask"]
                spot = data["data"]["spot"]
                change = data["data"]["change"]

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

asyncio.run(connect_to_websocket())