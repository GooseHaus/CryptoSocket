import React from 'react';
import { Coin } from '../types/coin';

type Props = {
    coins: Coin[];
};

const CoinsTable: React.FC<Props> = ({ coins }) => {
    // Sort by unix_timestamp in descending order
    const sortedCoins = [...coins].sort((a, b) => b.unix_timestamp - a.unix_timestamp);
    console.log("Rendering CoinsTable with coins:", sortedCoins);

    return (
        <table>
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Bid</th>
                    <th>Ask</th>
                    <th>Spot</th>
                    <th>Change</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                {sortedCoins.map((coin) => (
                    <tr key={coin.symbol_text + coin.unix_timestamp}>
                        <td>{coin.symbol_text}</td>
                        <td>{coin.bid_price}</td>
                        <td>{coin.ask_price}</td>
                        <td>{coin.spot_price}</td>
                        <td>{coin.price_change_24hr}</td>
                        <td>{coin.unix_timestamp}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default CoinsTable;
