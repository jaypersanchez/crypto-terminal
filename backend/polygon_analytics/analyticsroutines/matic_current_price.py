from pycoingecko import CoinGeckoAPI

def get_current_price():
    # Initialize the CoinGecko API client
    cg = CoinGeckoAPI()

    # Fetch current data for MATIC
    matic_data = cg.get_coin_by_id(id='matic-network')

    # Extract price, market cap, and volume in USD
    matic_price_usd = matic_data['market_data']['current_price']['usd']
    matic_market_cap_usd = matic_data['market_data']['market_cap']['usd']
    matic_volume_usd = matic_data['market_data']['total_volume']['usd']

    # Return formatted string with MATIC data
    return (f"Current Price of MATIC in USD: ${matic_price_usd}",
            f"Market Cap of MATIC in USD: ${matic_market_cap_usd}",
            f"24h Trading Volume of MATIC in USD: ${matic_volume_usd}")

# Example usage
current_price, market_cap, volume = get_current_price()
print(current_price)
print(market_cap)
print(volume)
