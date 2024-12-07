import asyncio, websockets, json, ssl

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

asyncio.run(connect_to_websocket())