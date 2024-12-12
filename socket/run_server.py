import uvicorn, os, django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cryptoSocket.settings")
django.setup()

if __name__ == "__main__":
    uvicorn.run(
        "cryptoSocket.asgi:application",  # Serve Django ASGI application
        host="127.0.0.1",
        port=8000,
        ssl_keyfile="key.pem",  # Path to your SSL key
        ssl_certfile="cert.pem",  # Path to your SSL certificate
    )