# DEPRECIATED BRANCH, remains for observational purposes only. Does not function. 
# Cryptocurrency WebSocket Service with Django Channels

This repository implements a **Django Channels**-based cryptocurrency rates server that provides real-time updates for various cryptocurrency assets in CAD (Canadian Dollars). The system leverages Django for enhanced scalability and flexibility, including WebSocket support for real-time cryptocurrency rates.

## Features

- **Real-Time Cryptocurrency Updates**: Fetches bid, ask, spot, and 24-hour price change data using the Binance API.
- **Currency Conversion**: Converts cryptocurrency prices from USD to CAD using Exchange Rate API.
- **WebSocket Subscription**: Allows clients to subscribe to a WebSocket endpoint for real-time updates.
- **Django Channels Integration**: Fully integrated with Django’s ASGI application architecture, making it easier to scale and manage.
- **Secure WebSocket Support**: Local development supports `wss://` for encrypted WebSocket communication.

## Requirements

- Python 3.8+
- Django 5.1+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  
   # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the WebSocket Server

1. Run the server using the provided `run_server.py` script from the `socket` directory to serve real-time cryptocurrency data over `wss://localhost:8000/markets/ws/`:

   ```bash
   cd socket
   python run_server.py
   ```

2. The server listens for WebSocket subscriptions and streams cryptocurrency data to connected clients.

### Connecting a WebSocket Client

1. Run the client to connect to the WebSocket server and subscribe to cryptocurrency rates. This will need to be done in a new shell window running in the same virtual environment:

   ```bash
   # Open a second shell window and move to the repo folder
   cd <repository_folder>

   # Start the virtual environment and run the client
   source venv/bin/activate
   cd socket
   python run_client.py
   ```

2. The client will print real-time cryptocurrency data received from the server.


## Project Structure

### Key Files

1. **`socket/get_crypto_dict.py`**:
   - Utility functions for cryptocurrency data:
     - Fetches bid, ask, spot, and 24-hour price change data from Binance API.
     - Converts USD to CAD using the Exchange Rate API.
     - Handles special cases for unsupported cryptocurrencies (e.g., USDT, QCAD, ETHW).
     - Formats data for WebSocket transmission.

2. **`socket/run_server.py`**:
   - Starts the WebSocket server using `uvicorn`.
   - Configures SSL for secure WebSocket communication.

3. **`socket/endpoint/consumers.py`**:
   - Implements the WebSocket consumer using Django Channels.
   - Handles client connections, subscriptions, and data streaming.

4. **`socket/endpoint/routing.py`**:
   - Defines WebSocket routes (e.g., `/markets/ws/`) for handling WebSocket connections.

5. **`socket/run_client.py`**:
   - Example WebSocket client script:
     - Connects to the server.
     - Subscribes to cryptocurrency rates.
     - Prints real-time updates.

## Notes

- The current implementation includes special handling for three unsupported cryptocurrencies (USDT, QCAD, ETHW).
- Ensure SSL certificates (`key.pem` and `cert.pem`) are available for local secure WebSocket testing.
- WebSocket traffic is served over `wss://localhost:8000/markets/ws/`.

## Future Enhancements

- Add a front-end UI for visualizing real-time cryptocurrency data.
- Imrove `fetch_*` functions in `get_crypto_dict.py` for efficiency, etc. 
- Improve error handling and resilience of the WebSocket server.
- Add test cases.
- Expand support for USDT, QCAD, ETHW. 
- Create models to store/update asset price values
