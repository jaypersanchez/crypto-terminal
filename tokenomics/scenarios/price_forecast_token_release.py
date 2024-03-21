'''
This module forecast the price change based on a target market cap and releasing 
supply at interval over 5 months
Console Run: python price_forecast_token_release.py 100000000 0.02 400000 20
'''
import argparse
import matplotlib.pyplot as plt

def forecast_price(initial_supply, initial_price, target_market_cap, total_tokens_for_trade, release_schedule):
    months_list = sorted(release_schedule.keys())  # Ensure months are in order
    circulating_supply = initial_supply * (total_tokens_for_trade / 100)
    prices = [initial_price]  # Starting price

    for month in months_list:
        circulating_supply += release_schedule[month]
        new_price = target_market_cap / circulating_supply
        prices.append(new_price)  # Append new price for each release

    # Ensure months_list starts from 0 for initial state
    months_list = [0] + months_list  

    plt.figure(figsize=(10, 6))
    plt.plot(months_list, prices, marker='o', linestyle='-')
    plt.title('Forecasted Token Price Over Time')
    plt.xlabel('Months')
    plt.ylabel('Price ($)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forecast token price based on release schedule.")
    parser.add_argument("initial_supply", type=int, help="Total initial supply of tokens.")
    parser.add_argument("initial_price", type=float, help="Initial price per token.")
    parser.add_argument("target_market_cap", type=int, help="Target market cap.")
    parser.add_argument("total_tokens_for_trade", type=int, help="Percentage of total tokens available for initial trade.")

    args = parser.parse_args()

    # Example release schedule; modify as needed or dynamically accept it
    release_schedule = {6: 10000000, 12: 5000000, 18: 5000000}

    forecast_price(args.initial_supply, args.initial_price, args.target_market_cap, args.total_tokens_for_trade, release_schedule)
