from pycoingecko import CoinGeckoAPI

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Fetch current data for Solana (SOL)
sol_data = cg.get_coin_by_id(id='solana')

# Extract price, market cap, and volume in USD
sol_price_usd = sol_data['market_data']['current_price']['usd']
sol_market_cap_usd = sol_data['market_data']['market_cap']['usd']
sol_volume_usd = sol_data['market_data']['total_volume']['usd']

print(f"Current Price of Solana (SOL) in USD: ${sol_price_usd}")
print(f"Market Cap of Solana (SOL) in USD: ${sol_market_cap_usd}")
print(f"24h Trading Volume of Solana (SOL) in USD: ${sol_volume_usd}")
