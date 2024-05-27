import sys
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Console Command: python sol_monthly_price_action.py "2022-09-01" "2022-09-30"
if len(sys.argv) < 3:
    print("Usage: python script_name.py <start_date> <end_date>")
    sys.exit(1)

start_date = sys.argv[1]
end_date = sys.argv[2]

# Simulating the process for Solana (SOL) as an example
# For actual data, replace the simulated data generation with real SOL data fetching logic
dates = pd.date_range(start=start_date, end=end_date)
prices = np.random.uniform(low=30, high=250, size=len(dates))  # Adjusted price range for SOL
df = pd.DataFrame(prices, index=dates, columns=['price'])

# Generate synthetic Open, High, and Low prices for SOL
df['open'] = df['price'] * np.random.uniform(0.95, 1.05, size=len(df))
df['high'] = df['price'] * np.random.uniform(1.02, 1.1, size=len(df))
df['low'] = df['price'] * np.random.uniform(0.9, 0.98, size=len(df))
df['close'] = df['price']

# Calculate SMAs
df['7_day_sma'] = df['close'].rolling(window=7).mean()
df['14_day_sma'] = df['close'].rolling(window=14).mean()

# Create a candlestick chart for SOL
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['price'])])

# Add SMAs to the figure
fig.add_trace(go.Scatter(x=df.index, y=df['7_day_sma'], mode='lines', name='7 Day SMA', line=dict(color='orange', width=1)))
fig.add_trace(go.Scatter(x=df.index, y=df['14_day_sma'], mode='lines', name='14 Day SMA', line=dict(color='purple', width=1)))

# Update layout with dynamic title based on passed dates for SOL
fig.update_layout(title=f'XRP (XRP) Price Movement - {start_date} to {end_date}',
                  xaxis_title='Date',
                  yaxis_title='Price (USD)',
                  xaxis_rangeslider_visible=False)  # Hide range slider

fig.show()
