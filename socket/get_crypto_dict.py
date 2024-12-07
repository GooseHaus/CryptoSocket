import requests, time, random

# List of assets. Unsupported as of Dec 6th: USDT, QCAD, ETHW. Workaround below. 
assets = [
    "BTC", "ETH", "LTC", "XRP", "BCH", "USDC", "XMR", "XLM",
    "USDT", "QCAD", "DOGE", "LINK", "MATIC", "UNI", "COMP", "AAVE", "DAI",
    "SUSHI", "SNX", "CRV", "DOT", "YFI", "MKR", "PAXG", "ADA", "BAT", "ENJ",
    "AXS", "DASH", "EOS", "BAL", "KNC", "ZRX", "SAND", "GRT", "QNT", "ETC",
    "ETHW", "1INCH", "CHZ", "CHR", "SUPER", "ELF", "OMG", "FTM", "MANA",
    "SOL", "ALGO", "LUNC", "UST", "ZEC", "XTZ", "AMP", "REN", "UMA", "SHIB",
    "LRC", "ANKR", "HBAR", "EGLD", "AVAX", "ONE", "GALA", "ALICE", "ATOM",
    "DYDX", "CELO", "STORJ", "SKL", "CTSI", "BAND", "ENS", "RNDR", "MASK",
    "APE"
]

# Function to get the current USD to CAD conversion rate from Exchange Rate API
def get_usd_to_cad_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    if 'rates' in data and 'CAD' in data['rates']:
        return data['rates']['CAD']

# Function to wrap each asset in the asset_CAD format required
def wrap_symbol(symbol):
    return symbol + "_CAD"

# Function to get unix time as an integer
def timestamp():
    return int(time.time())

# Function to fetch the current bid price from Binance API
def fetch_bid_price(symbol):
    """Fetch the best bid and ask prices for a given symbol from Binance."""
    url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    bid_price = data.get('bidPrice')
    if bid_price:
        bid_price = round(float(bid_price) * get_usd_to_cad_rate(), 2)
    return bid_price

# Function to fetch the current ask price from Binance API
def fetch_ask_price(symbol):
    """Fetch the best bid and ask prices for a given symbol from Binance."""
    url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    ask_price = data.get('askPrice')
    if ask_price:
        ask_price = round(float(ask_price) * get_usd_to_cad_rate(), 2)
    return ask_price

# Function to fetch the current spot price from Binance API
def fetch_spot_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    spot_price = data.get('price')
    if spot_price:
        spot_price = round(float(spot_price) * get_usd_to_cad_rate(), 2)
    return spot_price

# Function to fetch 24-hour price change from Binance API
def fetch_24hr_change(symbol):
    """Fetch the 24-hour price change for a given symbol from Binance."""
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    price_change = data.get('priceChange')
    if price_change:
        price_change = round(float(price_change) * get_usd_to_cad_rate(), 2)
    return price_change

# Function to build the dict for the websocket to eventually deliver
def build_dict(symbol):
    crypto_dict = {
        "channel": "rates",
        "event": "data",
        "data": {
            "symbol": wrap_symbol(symbol), 
            "timestamp": timestamp(), 
            "bid": fetch_bid_price(symbol), 
            "ask": fetch_ask_price(symbol), 
            "spot": fetch_spot_price(symbol), 
            "change": fetch_24hr_change(symbol)
        }
    }
    return crypto_dict

# Function to get a random asset's dictionary for the server
# 3 assets have workarounds, the rest work as intended
def get_random_dict():
    random_asset = random.choice(assets)

    # workaround for USDT, a USD stablecoin
    if random_asset == "USDT":
        num = get_usd_to_cad_rate()
        return {
            "channel": "rates",
            "event": "data",
            "data": {
                "symbol": "USDT_CAD", 
                "timestamp": timestamp(), 
                "bid": num, 
                "ask": num, 
                "spot": num, 
                "change": 0
                # change should be the delta in the exchange rate in the last 24hrs
            }
        }
    
    # workaround for QCAD, a CAD stablecoin
    elif random_asset == "QCAD":
        return {
            "channel": "rates",
            "event": "data",
            "data": {
                "symbol": "QCAD_CAD", 
                "timestamp": timestamp(), 
                "bid": 1, 
                "ask": 1, 
                "spot": 1, 
                "change": 0
            }
        }
    
    # workaround for ETHW, this one needs updating more than the others
    # synthesized from manual update of spot price, last update Dec 6th
    elif random_asset == "ETHW":
        spot = 5.02
        return {
            "channel": "rates",
            "event": "data",
            "data": {
                "symbol": "ETHW_CAD", 
                "timestamp": timestamp(), 
                "bid": round(random.uniform(spot*0.9, spot*1.1), 2), 
                "ask": round(random.uniform(spot*0.9, spot*1.1), 2), 
                "spot": round(spot * get_usd_to_cad_rate(), 2), 
                "change": round(random.uniform(spot*0.5, spot*1.5), 2)
            }
        }
    
    # the rest all work as intended
    else:
        return build_dict(random_asset)
