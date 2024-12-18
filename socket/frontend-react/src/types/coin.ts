export interface Coin {
    symbol_text: string;
    bid_price: number;
    ask_price: number;
    spot_price: number;
    price_change_24hr: number;
    unix_timestamp: number;
}