import sys
import time
import pycoingecko
import numpy as np

# Initialize PyCoinGecko client
cg = pycoingecko.CoinGeckoAPI()

# Function to retrieve historical market data for a given cryptocurrency
def get_historical_data(coin_id, currency, days):
    historical_data = cg.get_coin_market_chart_range_by_id(coin_id, currency, 'day', days)
    prices = [entry[1] for entry in historical_data['prices']]
    return prices

# Function to calculate the moving average
def calculate_moving_average(data, window_size):
    weights = np.repeat(1.0, window_size) / window_size
    return np.convolve(data, weights, 'valid')

# Function to determine trading signal based on moving average crossover strategy
def determine_signal(prices, short_window, long_window):
    short_ma = calculate_moving_average(prices, short_window)
    long_ma = calculate_moving_average(prices, long_window)

    if short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]:
        return 'BUY'
    elif short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]:
        return 'SELL'
    else:
        return 'HOLD'

# Main function
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['bitcoin', 'ethereum', 'solana', 'matic-network', 'ripple']:
        print("Usage: python trading_bot.py <crypto_id>")
        print("Supported crypto IDs: bitcoin, ethereum, solana, matic-network, ripple")
        return

    crypto_id = sys.argv[1]
    currency = 'usd'     # Example: USD
    short_window = 20     # Short moving average window size
    long_window = 50      # Long moving average window size

    while True:
        try:
            # Retrieve historical data
            prices = get_historical_data(crypto_id, currency, long_window)

            # Determine trading signal
            signal = determine_signal(prices, short_window, long_window)
            
            print(f'Trading signal for {crypto_id.capitalize()}: {signal}')

            # Sleep for some time before the next iteration
            time.sleep(60)  # Sleep for 1 minute (adjust as needed)
        
        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    main()
