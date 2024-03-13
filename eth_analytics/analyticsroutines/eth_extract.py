from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Calculate the date 3 months ago from today dynamically
three_months_ago = (datetime.today() - timedelta(days=90)).strftime('%d-%m-%Y')

# Get historical data for Ethereum (ETH) up to the current date
eth_data = cg.get_coin_market_chart_range_by_id(id='ethereum',
                                                vs_currency='usd',
                                                from_timestamp=datetime.strptime(three_months_ago, '%d-%m-%Y').timestamp(),
                                                to_timestamp=datetime.now().timestamp())

# Extracting price data
prices = eth_data['prices']

# Creating a DataFrame
df = pd.DataFrame(prices, columns=['timestamp', 'price'])

# Convert timestamp to datetime for readability
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Drop the original timestamp column as it's no longer needed
df.drop('timestamp', axis=1, inplace=True)

# Set the date as the index for easier analysis and plotting
df.set_index('date', inplace=True)

# Display the DataFrame
print(df)

# Optionally, save the data to a CSV file for offline analysis or backup
df.to_csv('./data/eth_daily_prices_last_3_months.csv')
