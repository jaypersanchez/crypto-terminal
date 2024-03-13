from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd
from coingecko_tools import *

valid_coin_ids = get_valid_coin_ids()
print(f'Top 10 coin details {valid_coin_ids[:10]}')  # Print the first 10 coin details for brevity

coin_id = 'bitcoin'  # Use the ID of the coin you're interested in
social_status = get_coin_social_status_by_id(coin_id)
print(social_status)

derivatives_info = get_derivatives()
print(derivatives_info)

btc_to_usd_rate = get_exchange_rate('btc')
# Print the exchange rate for Bitcoin to USD as an example
if btc_to_usd_rate:
    print("Bitcoin to USD exchange rate:", btc_to_usd_rate['value'], btc_to_usd_rate['unit'])
    
trending_cryptos = get_v3_search_trending()
print(trending_cryptos)
