from pycoingecko import CoinGeckoAPI
import pandas as pd

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

# Get current data for Ethereum (ETH)
eth_current_data = cg.get_price(ids='ethereum', vs_currencies='usd')

# Extracting current price
eth_price_usd = eth_current_data['ethereum']['usd']

# Creating a DataFrame for display
df = pd.DataFrame([{'currency': 'ETH', 'current_price_usd': eth_price_usd}])

# Display the DataFrame
print(df)

# Optionally, save the data to a CSV file for offline analysis or backup
df.to_csv('./data/eth_current_price.csv', index=False)
