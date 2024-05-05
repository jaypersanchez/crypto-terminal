import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(df):
    try:
        # Load the dataset from JSON file
        df = pd.read_json(df)
        
        print("Preparing features and labels")
        X = df.drop('input', axis=1)
        y = df['input']
        print(df.head())
        
        print("Splitting dataset.....")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
    except Exception as e:
        print( f"Training set shape: {X_train.shape}, {y_train.shape}")

# If we want to test this file as standalone
if __name__ == "__main__":
    df = 'sentiment_dataset.json'
    X_train, X_test, y_train, y_test = preprocess_data(df)
    if X_train is not None:
        print(f"Training set shape: {X_train.shape}, {y_train.shape}")
        print(f"Testing set shape: {X_test.shape}, {y_test.shape}")
    else:
        print("Preprocessing failed.")