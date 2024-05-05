'''
This SOL data extract can be run at anytime since it will take
the most recent trading date and extract data the next day up to the current date.
This way, this can be run at anytime and it will be sure to get the most recent data.
'''
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Load the existing data to find the most recent date
existing_df = pd.read_csv('../../data/sol_yearly_extract_exchange_data.csv')
latest_date_str = existing_df['date'].max()  # Get the latest date in string format
latest_date = datetime.strptime(latest_date_str, '%Y-%m-%d')  # Convert to datetime object

# Calculate the start date for new data extraction (one day after the latest date)
start_date = latest_date + timedelta(days=1)

# Define the end date for data extraction (today)
end_date = datetime.now()

# Format dates for the API call
from_timestamp = int(start_date.timestamp())
to_timestamp = int(end_date.timestamp())

# Get historical data for Solana (SOL) starting from one day after the latest date in the CSV up to the current date
sol_data = cg.get_coin_market_chart_range_by_id(
    id='solana',
    vs_currency='usd',
    from_timestamp=from_timestamp,
    to_timestamp=to_timestamp
)

# Extract price and volume data
prices = sol_data['prices']
volumes = sol_data['total_volumes']

# Creating DataFrames for prices and volumes with 'date' column
df_prices = pd.DataFrame(prices, columns=['timestamp', 'price'])
df_prices['date'] = pd.to_datetime(df_prices['timestamp'], unit='ms').dt.date

df_volumes = pd.DataFrame(volumes, columns=['timestamp', 'volume'])
df_volumes['date'] = pd.to_datetime(df_volumes['timestamp'], unit='ms').dt.date

# Merging the dataframes on the 'date' column
df_merged = pd.merge(df_prices, df_volumes, on='date')

# Dropping 'timestamp' columns
df_merged.drop(['timestamp_x', 'timestamp_y'], axis=1, inplace=True)

# Group by 'date' to aggregate data
df_grouped = df_merged.groupby('date').agg(
    open_price=('price', 'first'),
    close_price=('price', 'last'),
    avg_volume=('volume', 'mean')
).reset_index()

# Append the new data to the existing CSV file
df_grouped.to_csv('../../data/sol_yearly_extract_exchange_data.csv', mode='a', header=False, index=False)

print("Data appended successfully to '../../data/sol_yearly_extract_exchange_data.csv'.")
