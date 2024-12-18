# Cryptocurrency WebSocket Service with Django Channels and React Frontend

This repository implements a **Django Channels**-based cryptocurrency rates server that provides real-time updates for various cryptocurrency assets in CAD (Canadian Dollars). It also includes a **React + TypeScript** frontend for visualizing cryptocurrency data.

## Features

- **Real-Time Cryptocurrency Updates**: Fetches bid, ask, spot, and 24-hour price change data using the Binance API.
- **Currency Conversion**: Converts cryptocurrency prices from USD to CAD using Exchange Rate API.
- **WebSocket Subscription**: Allows clients to subscribe to a WebSocket endpoint for real-time updates.
- **Django Channels Integration**: Fully integrated with Django’s ASGI application architecture for scalability and real-time functionality.
- **React Frontend**: Displays both historical data and real-time updates using WebSocket subscriptions.
- **Secure WebSocket Support**: Local development supports `wss://` for encrypted WebSocket communication.

---

## Requirements

- Python 3.8+
- Django 5.1+
- Node.js 16+ and npm
- Dependencies listed in `requirements.txt`

---

## Installation

### Backend Setup

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

4. Setup the database to store coin values:
   ```bash
   cd socket
   python manage.py migrate
   ```

4. Start the backend server (WebSocket + REST API):
   ```bash
   python run_server.py
   ```

### Frontend Setup

1. Navigate to the `frontend-react` folder:
   ```bash
   cd ../frontend-react
   ```

2. Install the dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open the frontend in your browser:
   ```
   http://localhost:5173
   ```

---

## Usage

### Backend

1. **WebSocket Endpoint**:
   - Serves real-time cryptocurrency data at `wss://localhost:8000/markets/ws/`.

2. **REST API Endpoint**:
   - Serves historical cryptocurrency data at `https://localhost:8000/api/coins/`.

### Frontend

- The React frontend connects to both the WebSocket and the REST API.
- Displays a table of historical cryptocurrency data on load.
- Updates the table in real-time as new data arrives from the WebSocket.

---

## Project Structure

### Backend

1. **`socket/get_crypto_dict.py`**:
   - Fetches cryptocurrency data and converts prices to CAD.
   - Formats data for WebSocket transmission.

2. **`socket/run_server.py`**:
   - Starts the WebSocket server using `uvicorn`.
   - Configures SSL for secure WebSocket communication.

3. **`socket/endpoint/consumers.py`**:
   - Handles WebSocket connections, subscriptions, and data streaming.

4. **`socket/endpoint/routing.py`**:
   - Defines WebSocket routes (e.g., `/markets/ws/`).

5. **`socket/endpoint/views.py`**:
   - Serves historical data via a REST API endpoint.

### Frontend

1. **`frontend-react/src/App.tsx`**:
   - Main React component that integrates data fetching, WebSocket updates, and the table UI.

2. **`frontend-react/src/components/CoinsTable.tsx`**:
   - Reusable table component to display cryptocurrency data.

3. **`frontend-react/src/types/coin.ts`**:
   - Defines TypeScript types for cryptocurrency data.

---

## Notes

- Ensure SSL certificates (`key.pem` and `cert.pem`) are available for local secure WebSocket testing.
- WebSocket traffic is served over `wss://localhost:8000/markets/ws/`.

---

## Future Enhancements

- Imrove `fetch_*` functions in `get_crypto_dict.py` for efficiency, etc. 
- Improve error handling and resilience of the WebSocket server.
- Add test cases.
- Expand support for USDT, QCAD, ETHW. 
- Create models to store/update asset price values
