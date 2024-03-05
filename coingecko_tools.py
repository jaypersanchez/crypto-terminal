from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd

cg = CoinGeckoAPI()

"""
Get valid coin id from CoinGecko
"""
def get_valid_coin_ids():
    cg = CoinGeckoAPI()
    coin_list = cg.get_coins_list()
    return coin_list

"""
Fetches social media data related to a specific coin, including Twitter followers, Reddit subscribers, 
and other social metrics. Sentiment analysis or models predicting price movements based on social media trends can benefit from this data.
"""
def get_coin_social_status_by_id(coin_id):
    cg = CoinGeckoAPI()
    # Fetch social media data for the specified coin
    coin_data = cg.get_coin_by_id(coin_id, localization='false', tickers=False, market_data=False, community_data=True, developer_data=False)
    
    # Extracting social data
    social_data = {
        "facebook_likes": coin_data['community_data']['facebook_likes'],
        "twitter_followers": coin_data['community_data']['twitter_followers'],
        "reddit_average_posts_48h": coin_data['community_data']['reddit_average_posts_48h'],
        "reddit_average_comments_48h": coin_data['community_data']['reddit_average_comments_48h'],
        "reddit_subscribers": coin_data['community_data']['reddit_subscribers'],
        "reddit_accounts_active_48h": coin_data['community_data']['reddit_accounts_active_48h'],
        "telegram_channel_user_count": coin_data['community_data'].get('telegram_channel_user_count')  # Some coins might not have Telegram data
    }

    return social_data

"""
Provides data on cryptocurrency derivatives, including futures and options. 
This advanced market data can be used to understand market sentiment, 
hedge against price movements, or explore arbitrage opportunities.
"""
def get_derivatives():
    cg = CoinGeckoAPI()
    # Fetch derivatives data
    derivatives_data = cg.get_derivatives()
    
    # Format or process the data as needed, for now, just return the raw data
    return derivatives_data

"""
Retrieves current exchange rates between cryptocurrencies and fiat currencies. 
This is crucial for applications that need real-time conversion rates or analyze 
the impact of exchange rate fluctuations on the cryptocurrency market._summary_
"""
def get_exchange_rate(currency_id='btc'):
    cg = CoinGeckoAPI()
    # Fetch exchange rates
    exchange_rates = cg.get_exchange_rates()
    
    # Extracting exchange rate data
    rates = exchange_rates['rates']
    
    # Check if the currency_id is available in the rates
    if currency_id in rates:
        # Print the exchange rate for the specified currency
        print(f"{currency_id.upper()} to USD:", rates[currency_id]['value'], rates[currency_id]['unit'])
    else:
        print(f"Exchange rate for {currency_id} not found.")

    return rates[currency_id] if currency_id in rates else None

"""
An updated method to retrieve trending search coins on CoinGecko as searched by users. 
This can be particularly useful for identifying emerging trends or coins gaining popularity.
OpenBB has something similar.  May be able to combine results for better analytics.
"""
def get_v3_search_trending():
    cg = CoinGeckoAPI()
    # Fetch trending cryptocurrency data
    trending = cg.get_search_trending()
    
    # Extracting information about trending coins
    trending_coins = trending['coins']
    trending_data = []
    
    for coin in trending_coins:
        coin_data = {
            "id": coin['item']['id'],
            "symbol": coin['item']['symbol'],
            "name": coin['item']['name'],
            "market_cap_rank": coin['item']['market_cap_rank'],
            "thumb": coin['item']['thumb'],  # Thumbnail image URL
            "score": coin['item']['score']  # Trending score
        }
        trending_data.append(coin_data)
    
    return trending_data
