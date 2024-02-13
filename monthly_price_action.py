import sys
import plotly.graph_objects as go
import pandas as pd
import numpy as np

if len(sys.argv) < 3:
    print("Usage: python script_name.py <start_date> <end_date>")
    sys.exit(1)

start_date = sys.argv[1]
end_date = sys.argv[2]

# Generate dates and prices within the specified range
dates = pd.date_range(start=start_date, end=end_date)
prices = np.random.uniform(low=1500, high=2000, size=len(dates))  # Simulated close prices
df = pd.DataFrame(prices, index=dates, columns=['price'])

# Generate synthetic Open, High, and Low prices
df['open'] = df['price'] * np.random.uniform(0.95, 1.05, size=len(df))
df['high'] = df['price'] * np.random.uniform(1.02, 1.1, size=len(df))
df['low'] = df['price'] * np.random.uniform(0.9, 0.98, size=len(df))

# Create a candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['price'])])

# Update layout with dynamic title based on passed dates
fig.update_layout(title=f'Ethereum Price Movement - {start_date} to {end_date}',
                  xaxis_title='Date',
                  yaxis_title='Price (USD)',
                  xaxis_rangeslider_visible=False)  # Hide range slider

fig.show()
