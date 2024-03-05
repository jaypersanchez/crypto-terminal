from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Calculate the date 3 months ago from today dynamically
#three_months_ago = (datetime.today() - timedelta(days=90)).strftime('%d-%m-%Y')
# Calculate the date 3 months ago from today dynamically
three_months_ago = (datetime.today() - timedelta(days=356)).strftime('%d-%m-%Y')

# Get historical data for Solana (SOL) up to the current date
sol_data = cg.get_coin_market_chart_range_by_id(
    id='solana',
    vs_currency='usd',
    from_timestamp=datetime.strptime(three_months_ago, '%d-%m-%Y').timestamp(),
    to_timestamp=datetime.now().timestamp()
)

# Extracting price data
prices = sol_data['prices']
volumes = sol_data['total_volumes']


# Creating a DataFrame for prices
df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
df_prices['date'] = pd.to_datetime(df_prices['timestamp'], unit='ms').dt.date

# Creating a DataFrame for volumes
df_volumes = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
df_volumes['date'] = pd.to_datetime(df_volumes['timestamp'], unit='ms').dt.date

# Merging the dataframes on the date
df_merged = pd.merge(df_prices, df_volumes, on='date')

# Drop the original timestamp columns as they are no longer needed
df_merged.drop(['timestamp_x', 'timestamp_y'], axis=1, inplace=True)

# Group by date to get the opening price (first price of the day), closing price (last price of the day), and average volume
df_grouped = df_merged.groupby('date').agg(
    open_price=('price', 'first'),
    close_price=('price', 'last'),
    avg_volume=('volume', 'mean')
).reset_index()

# Setting date as the index
df_grouped.set_index('date', inplace=True)

# Display the DataFrame
print(df_grouped)

# Optionally, save the data to a CSV file for offline analysis or backup
df_grouped.to_csv('../data/sol_exchange_data_yearly.csv')
