import uvicorn

# Simplified script for running the uvicorn server using ssl
if __name__ == "__main__":
    uvicorn.run(
        "cryptoSocket.asgi:application",
        host="127.0.0.1",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
    )