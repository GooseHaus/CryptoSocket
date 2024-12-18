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
                setCoins(data);
            } catch (error) {
                console.error("Error fetching initial data:", error);
            }
        };

        fetchInitialData();
    }, []);

    // WebSocket connection for live updates
    useEffect(() => {
        const socket = new WebSocket("wss://localhost:8000/markets/ws/");

        socket.onopen = () => {
            console.log("WebSocket connected");
            setStatus("Connected");
            socket.send(JSON.stringify({ event: "subscribe", channel: "rates" }));
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log("Message received:", message);
            if (message.channel === "rates" && message.event === "data") {
                const newCoin: Coin = message.data;

                setCoins((prevCoins) => {
                    const index = prevCoins.findIndex(coin => coin.symbol_text === newCoin.symbol_text);
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

        socket.onclose = () => {
            console.log("WebSocket disconnected");
            setStatus("Disconnected");
        };

        return () => socket.close();
    }, []);

    return (
        <div>
            <h1>Market Rates</h1>
            <p>Status: {status}</p>
            <CoinsTable coins={coins} />
        </div>
    );
};

export default App;
