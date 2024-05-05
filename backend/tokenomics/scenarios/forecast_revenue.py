'''
This provides a visual of revenue of pre-sale and public sale based on initial supply
with 30% allocations and initial price
Console Run: python forecast_revenue.py 100000000 0.02
'''
import argparse
import matplotlib.pyplot as plt

def calculate_revenue(initial_supply, initial_price, distribution_percentages):
    distribution = {key: initial_supply * (percent / 100) for key, percent in distribution_percentages.items()}
    pre_sale_revenue = distribution['pre_sale'] * initial_price
    public_sale_revenue = distribution['public_sale'] * initial_price
    return distribution, pre_sale_revenue, public_sale_revenue

def plot_revenue(pre_sale_revenue, public_sale_revenue):
    categories = ['Pre-Sale Revenue', 'Public Sale Revenue']
    values = [pre_sale_revenue, public_sale_revenue]
    
    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color=['blue', 'green'])
    plt.title('Token Sale Revenue')
    plt.ylabel('Revenue ($)')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate and plot potential revenue from token sales.")
    parser.add_argument("initial_supply", type=int, help="Initial token supply.")
    parser.add_argument("initial_price", type=float, help="Initial token price.")
    
    args = parser.parse_args()

    distribution_percentages = {'pre_sale': 30, 'public_sale': 70}
    distribution, pre_sale_revenue, public_sale_revenue = calculate_revenue(args.initial_supply, args.initial_price, distribution_percentages)
    
    print(f"Distribution: {distribution}")
    print(f"Pre-Sale Revenue: ${pre_sale_revenue}")
    print(f"Public Sale Revenue: ${public_sale_revenue}")

    plot_revenue(pre_sale_revenue, public_sale_revenue)
