'''
Console Run: python price_effect_burn_marketcap_console.py --initial_supply 100000000 --initial_price 0.02 --max_burn 50000000 --step 5000000
'''
import argparse
import matplotlib.pyplot as plt

def calculate_market_cap(initial_supply, initial_price, burn_amount):
    new_supply = initial_supply - burn_amount
    new_price = initial_price * (initial_supply / new_supply)
    new_market_cap = new_supply * new_price
    return new_market_cap, new_price

def plot_market_impact(initial_supply, initial_price, max_burn, step):
    burn_amounts = range(0, max_burn + 1, step)
    market_caps = []
    prices = []

    for burn in burn_amounts:
        new_market_cap, new_price = calculate_market_cap(initial_supply, initial_price, burn)
        market_caps.append(new_market_cap)
        prices.append(new_price)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Burn Amount')
    ax1.set_ylabel('Market Cap ($)', color=color)
    ax1.plot(burn_amounts, market_caps, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('Price ($)', color=color)
    ax2.plot(burn_amounts, prices, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Effect of Token Burn on Market Cap and Price')
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot the impact of token burn on market cap and price.')
    parser.add_argument('--initial_supply', type=int, help='Initial token supply', required=True)
    parser.add_argument('--initial_price', type=float, help='Initial token price', required=True)
    parser.add_argument('--max_burn', type=int, help='Maximum token burn amount', required=True)
    parser.add_argument('--step', type=int, help='Step size for token burn amounts', required=True)

    args = parser.parse_args()
    
    plot_market_impact(args.initial_supply, args.initial_price, args.max_burn, args.step)
