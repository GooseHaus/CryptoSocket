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

// Function to populate the table with initial data
async function fetchInitialData() {
    try {
        const response = await fetch("https://localhost:8000/api/coins/");
        const data = await response.json();

        data.forEach((coin) => {
            const row = `
                <tr data-symbol="${coin.symbol_text}">
                    <td>${coin.symbol_text}</td>
                    <td>${coin.bid_price}</td>
                    <td>${coin.ask_price}</td>
                    <td>${coin.spot_price}</td>
                    <td>${coin.price_change_24hr}</td>
                </tr>
            `;
            ratesEl.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        console.error("Error fetching initial data:", error);
    }
}

// Fetch initial data
fetchInitialData();

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

        // Check if a row with the symbol already exists
        let existingRow = document.querySelector(`#rates tr[data-symbol="${data.symbol}"]`);

        if (existingRow) {
            // Update the existing row
            existingRow.innerHTML = `
                <td>${data.symbol}</td>
                <td>${data.bid}</td>
                <td>${data.ask}</td>
                <td>${data.spot}</td>
                <td>${data.change}</td>
            `;
        } else {
            // Append a new row if the symbol is new
            const row = `
                <tr data-symbol="${data.symbol}">
                    <td>${data.symbol}</td>
                    <td>${data.bid}</td>
                    <td>${data.ask}</td>
                    <td>${data.spot}</td>
                    <td>${data.change}</td>
                </tr>
            `;
            ratesEl.insertAdjacentHTML("beforeend", row);
        }
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
