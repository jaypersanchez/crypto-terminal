import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

# Linear Regression Data Analytics

# Load the ETH data from the CSV file
df = pd.read_csv('./data/eth_daily_prices_last_3_months.csv', parse_dates=['date'])
df['date_ordinal'] = df['date'].map(datetime.toordinal)  # Convert dates to numerical format

# Reshape data for scikit-learn
X = df['date_ordinal'].values.reshape(-1, 1)  # Independent variable
y = df['price'].values  # Dependent variable

# Create and fit the model
model = LinearRegression()
model.fit(X, y)

# Coefficients
print(f"Coefficient: {model.coef_[0]}, Intercept: {model.intercept_}")

# Create a DataFrame for plotting
df_plot = pd.DataFrame({'date': df['date'], 'actual_price': y})

# Predict prices using the model for plotting
df_plot['predicted_price'] = model.predict(X)

# Plotting
plt.figure(figsize=(10, 6))
sns.lineplot(x='date', y='actual_price', data=df_plot, label='Actual Price', color='blue')
sns.lineplot(x='date', y='predicted_price', data=df_plot, label='Predicted Price', color='red')

plt.title('ETH Price and Linear Regression Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
