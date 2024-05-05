'''
This scenario provides visual insight on price effect 
based on initial price and burn amount
'''
import matplotlib.pyplot as plt

# Function to calculate new price
def calculate_new_price(initial_supply, initial_price, burn_amount):
    new_supply = initial_supply - burn_amount
    new_price = initial_price * (initial_supply / new_supply)
    return new_price

initial_supply = 100000000  # 100M
initial_price = 0.02  # $0.02
burn_amounts = range(0, 50000001, 5000000)  # Up to 50M tokens in 5M steps

# Calculate new prices for each burn amount
new_prices = [calculate_new_price(initial_supply, initial_price, burn) for burn in burn_amounts]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(burn_amounts, new_prices, marker='o')
plt.title('Effect of Token Burn on Price')
plt.xlabel('Burn Amount')
plt.ylabel('New Price ($)')
plt.grid(True)
plt.show()
