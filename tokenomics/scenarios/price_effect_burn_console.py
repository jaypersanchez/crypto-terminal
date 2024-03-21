'''
This scenario provides visual insight on price effect 
based on initial price and burn amount
Console run: python price_effect_burn_console.py --initial_supply 100000000 --initial_price 0.02 --max_burn 50000000 --step 5000000
'''
import argparse
import matplotlib.pyplot as plt

def calculate_new_price(initial_supply, initial_price, burn_amount):
    new_supply = initial_supply - burn_amount
    new_price = initial_price * (initial_supply / new_supply)
    return new_price

def plot_price_impact(initial_supply, initial_price, burn_amounts):
    new_prices = [calculate_new_price(initial_supply, initial_price, burn) for burn in burn_amounts]
    plt.figure(figsize=(10, 6))
    plt.plot(burn_amounts, new_prices, marker='o')
    plt.title('Effect of Token Burn on Price')
    plt.xlabel('Burn Amount')
    plt.ylabel('New Price ($)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot the impact of token burn on price.')
    parser.add_argument('--initial_supply', type=int, help='Initial token supply', required=True)
    parser.add_argument('--initial_price', type=float, help='Initial token price', required=True)
    parser.add_argument('--max_burn', type=int, help='Maximum token burn amount', required=True)
    parser.add_argument('--step', type=int, help='Step size for token burn amounts', required=True)

    args = parser.parse_args()

    burn_amounts = range(0, args.max_burn + 1, args.step)
    plot_price_impact(args.initial_supply, args.initial_price, burn_amounts)
