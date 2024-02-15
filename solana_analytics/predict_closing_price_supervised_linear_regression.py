from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data_path = "../data/sol_exchange_data_yearly.csv"
df = pd.read_csv(data_path)

# Prepare the dataset
X = df[['open_price', 'avg_volume']]  # Features
y = df['close_price']                 # Target

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and evaluate
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"RMSE: {rmse}")

# Model coefficients
print(f"Coefficients: {model.coef_}")

# Plotting the results
# Scatter plot of actual vs. predicted prices
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=predictions, alpha=0.6)
sns.lineplot(x=y_test, y=y_test, color='red', label='Actual')
plt.title('Actual vs. Predicted Close Prices')
plt.xlabel('Actual Close Price')
plt.ylabel('Predicted Close Price')
plt.legend()
plt.show(block=False)

# If desired, plot the relationship between open_price, avg_volume, and close_price
fig, axs = plt.subplots(1, 2, figsize=(15, 6))
sns.scatterplot(x='open_price', y='close_price', data=df, ax=axs[0], color='skyblue', label='Open Price vs Close Price')
sns.scatterplot(x='avg_volume', y='close_price', data=df, ax=axs[1], color='lightgreen', label='Avg Volume vs Close Price')
axs[0].set_title('Open Price vs Close Price')
axs[1].set_title('Avg Volume vs Close Price')
plt.show()