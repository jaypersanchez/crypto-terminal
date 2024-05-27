# Linear Regression with two independent variable 'open_price' and 'avg_volume'

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data_path = "../data/xrp_yearly_extract_exchange_data.csv"
df = pd.read_csv(data_path)

# Selecting the features and the label
X = df[['open_price', 'avg_volume']]  # Now using two independent variables
y = df['close_price']  # Dependent variable

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize and train the linear regression model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Make predictions on the test data
predictions = lr.predict(X_test)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"Root Mean Squared Error (RMSE) on test data: {rmse}")

# Show model coefficients
print(f"Coefficients: {lr.coef_}, Intercept: {lr.intercept_}")

# Example of making a prediction based on user input
open_price_input = float(input("Enter an opening price to predict the closing price: "))
avg_volume_input = float(input("Enter average volume to predict the closing price: "))
new_data = [[open_price_input, avg_volume_input]]
new_prediction = lr.predict(new_data)
print(f"Predicted close price for given data: {new_prediction[0]}")


# Plotting with Seaborn
# Scatter plot for actual data
sns.scatterplot(x=X_train['open_price'], y=y_train, color='blue', label='Training Data')
sns.scatterplot(x=X_test['open_price'], y=y_test, color='green', label='Test Data')

# Scatter plot for actual data against open_price
sns.scatterplot(x=X_train['open_price'], y=y_train, color='blue', label='Training Data')
sns.scatterplot(x=X_test['open_price'], y=y_test, color='green', label='Test Data')
plt.title('Open Price vs. Closing Price (Partial View)')
plt.xlabel('Open Price')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

