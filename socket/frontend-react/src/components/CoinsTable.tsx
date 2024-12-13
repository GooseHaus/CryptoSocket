import React from 'react';
import { Coin } from '../types/coin';

interface CoinsTableProps {
    coins: Coin[];
}

const CoinsTable: React.FC<CoinsTableProps> = ({ coins }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Bid</th>
                    <th>Ask</th>
                    <th>Spot</th>
                    <th>Change</th>
                </tr>
            </thead>
            <tbody>
                {coins.map((coin, index) => (
                    <tr key={index}>
                        <td>{coin.symbol_text}</td>
                        <td>{coin.bid_price}</td>
                        <td>{coin.ask_price}</td>
                        <td>{coin.spot_price}</td>
                        <td>{coin.price_change_24hr}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default CoinsTable;
