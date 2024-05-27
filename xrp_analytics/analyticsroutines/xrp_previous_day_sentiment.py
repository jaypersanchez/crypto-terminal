from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Calculate the date 3 months ago from today dynamically
three_months_ago = (datetime.today() - timedelta(days=90)).strftime('%d-%m-%Y')

# Get historical data for Solana (SOL) up to the current date
sol_data = cg.get_coin_market_chart_range_by_id(id='ripple',
                                                vs_currency='usd',
                                                from_timestamp=datetime.strptime(three_months_ago, '%d-%m-%Y').timestamp(),
                                                to_timestamp=datetime.now().timestamp())

# Extracting price data
prices = sol_data['prices']

# Creating a DataFrame
df = pd.DataFrame(prices, columns=['timestamp', 'price'])

# Convert timestamp to datetime for readability
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Calculate daily price change
df['price_change'] = df['price'].diff()

# Determine sentiment based on price change
df['sentiment'] = df['price_change'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral'))

# Drop unnecessary columns (timestamp and price_change)
df.drop(['timestamp', 'price_change'], axis=1, inplace=True)

# Set the date as the index for easier analysis
df.set_index('date', inplace=True)

# Visualize sentiment distribution using Seaborn
plt.figure(figsize=(10, 6))
sns.countplot(x='sentiment', data=df, palette='viridis')
plt.title('XRP Price Sentiment Distribution Over the Last 3 Months')
plt.xlabel('Sentiment')
plt.ylabel('Frequency')
plt.show()
