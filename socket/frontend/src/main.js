import './style.css';

// Create and display status element
const statusEl = document.createElement("p");
statusEl.textContent = "Status: Disconnected";
document.body.appendChild(statusEl);

// Create and display table
const table = document.createElement("table");
table.innerHTML = `
    <thead>
        <tr>
            <th>Symbol</th>
            <th>Timestamp</th>
            <th>Bid</th>
            <th>Ask</th>
            <th>Spot</th>
            <th>Change</th>
        </tr>
    </thead>
    <tbody id="rates"></tbody>
`;
document.body.appendChild(table);

const ratesEl = document.getElementById("rates");

// Set up WebSocket connection
const socket = new WebSocket("wss://localhost:8000/markets/ws/");

socket.onopen = () => {
    console.log("WebSocket connected");
    statusEl.textContent = "Status: Connected";

    // Subscribe to the rates channel
    socket.send(JSON.stringify({ event: "subscribe", channel: "rates" }));
};

socket.onmessage = (event) => {
    const message = JSON.parse(event.data);

    if (message.channel === "rates" && message.event === "data") {
        const data = message.data;

        // Append new row to the table
        const row = `
            <tr>
                <td>${data.symbol}</td>
                <td>${new Date(data.timestamp).toLocaleTimeString()}</td>
                <td>${data.bid}</td>
                <td>${data.ask}</td>
                <td>${data.spot}</td>
                <td>${data.change}</td>
            </tr>
        `;
        ratesEl.insertAdjacentHTML("beforeend", row);
    }
};

socket.onerror = (error) => {
    console.error("WebSocket error:", error);
    statusEl.textContent = "Status: Error";
};

socket.onclose = () => {
    console.log("WebSocket connection closed");
    statusEl.textContent = "Status: Disconnected";
};