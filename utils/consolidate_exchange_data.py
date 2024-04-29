import pandas as pd
from sklearn.preprocessing import StandardScaler
import pymongo
import os

def load_and_consolidate_data(file_paths):
    data_frames = []
    for crypto, file_path in file_paths.items():
        df = pd.read_csv(file_path)
        df['crypto'] = crypto  # Add a column to identify the cryptocurrency
        data_frames.append(df)
    consolidated_df = pd.concat(data_frames, ignore_index=True)
    return consolidated_df

def normalize_data(df, columns_to_scale):
    scaler = StandardScaler()
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df

def save_data_to_mongo(df, db_name, collection_name):
    # MongoDB connection
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]

    # Convert DataFrame to dictionary format for MongoDB insertion
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)
    print(f"Data successfully saved to MongoDB database '{db_name}' in collection '{collection_name}'")

# File paths
file_paths = {
    'BTC': '../data/btc_yearly_extract_exchange_data.csv',
    'ETH': '../data/eth_yearly_extract_exchange_data.csv',
    'SOL': '../data/sol_yearly_extract_exchange_data.csv',
    'MATIC': '../data/matic_yearly_extract_exchange_data.csv'
}

# Consolidate and Normalize Data
consolidated_data = load_and_consolidate_data(file_paths)
normalized_data = normalize_data(consolidated_data, ['open_price', 'close_price', 'avg_volume'])

# Save to MongoDB
save_data_to_mongo(normalized_data, 'crypto-terminal', 'ai_training_data')
