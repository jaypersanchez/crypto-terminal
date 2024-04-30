import pymongo
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['crypto-terminal']
collection = db['ai_training_data']

# Fetch data and convert to DataFrame
documents = list(collection.find({}))
data = pd.DataFrame(documents)
data.drop(columns=['_id'], inplace=True)

# Prepare features and target for machine learning
features = data[['open_price', 'close_price', 'avg_volume']]
target = data['close_price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Model evaluation
print("Training score:", model.score(X_train, y_train))
print("Testing score:", model.score(X_test, y_test))

# Clean up: close MongoDB connection
client.close()
