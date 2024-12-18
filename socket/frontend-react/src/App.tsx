import React, { useEffect, useState } from 'react';
import CoinsTable from './components/CoinsTable';
import './App.css';
import { Coin } from './types/coin';

const App: React.FC = () => {
    const [coins, setCoins] = useState<Coin[]>([]);
    const [status, setStatus] = useState<string>("Disconnected");

    // Fetch initial data from the REST API
    useEffect(() => {
    const fetchInitialData = async () => {
        try {
            const response = await fetch("https://localhost:8000/api/coins/");
            const data: Coin[] = await response.json();
            console.log("Initial data fetched:", data);
            setCoins(data); // Populate the table with initial data
        } catch (error) {
            console.error("Error fetching initial data:", error);
        }
    };

    fetchInitialData();
}, []); // Empty dependency ensures it runs only once

    // WebSocket connection for live updates
    useEffect(() => {
        let socket: WebSocket | null = null;
        let reconnectAttempts = 0;
    
        const connectWebSocket = () => {
            console.log("Attempting to connect WebSocket...");
            socket = new WebSocket("wss://localhost:8000/markets/ws/");
    
            socket.onopen = () => {
                console.log("WebSocket connected");
                setStatus("Connected");
                reconnectAttempts = 0; // Reset attempts on successful connection
                socket?.send(JSON.stringify({ event: "subscribe", channel: "rates" }));
            };
    
            socket.onmessage = (event) => {
                console.log("Message received:", event.data);
                const message = JSON.parse(event.data);
                console.log("Parsed message:", message);
                
                if (message.channel === "rates" && message.event === "data") {
                    const newCoin: Coin = message.data;
            
                    setCoins((prevCoins) => {
                        const index = prevCoins.findIndex(
                            (coin) => coin.symbol_text === newCoin.symbol_text
                        );
                        console.log("Updated coins state after WebSocket message:", coins);
            
                        if (index !== -1) {
                            // Update existing coin
                            const updatedCoins = [...prevCoins];
                            updatedCoins[index] = newCoin;
                            return updatedCoins;
                        } else {
                            // Add new coin
                            return [...prevCoins, newCoin];
                        }
                        
                    });
                }
            };
    
            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
                setStatus("Error");
            };
    
            socket.onclose = (event) => {
                console.log(`WebSocket disconnected: ${event.code}`);
                setStatus("Disconnected");
                socket = null; // Ensure no dangling reference
    
                // Attempt reconnection with backoff
                const timeout = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000); // Cap at 30s
                reconnectAttempts += 1;
                setTimeout(connectWebSocket, timeout);
            };
        };
    
        connectWebSocket();
    
        // Cleanup function to ensure the WebSocket is closed properly
        return () => {
            console.log("Cleaning up WebSocket connection");
            if (socket) {
                socket.close();
                socket = null;
            }
        };
    }, []); // Only run once when the component mounts

    return (
        <div>
            <h1>Market Rates</h1>
            <p>Status: {status}</p>
            <CoinsTable coins={coins} />
        </div>
    );
};

export default App;
