from flask import Flask, jsonify, request
from pycoingecko import CoinGeckoAPI
from flask_cors import CORS
import pymongo
import pandas as pd
import os
import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.linear_model import LinearRegression
import numpy as np
from dotenv import load_dotenv
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
from web3 import Web3

app = Flask(__name__)
CORS(app)
# Load environment variables from .env file
load_dotenv()
# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Closing price prediction for the next 7 days based latest data
@app.route('/forecast', methods=['POST'])
def fetch_crypto_data():
    data = request.get_json()
    crypto_name = data.get('crypto_name')
    print(f"crypto_name {crypto_name}")
    if not crypto_name:
        return jsonify({'error': 'crypto_name parameter is required'}), 400

    # Mapping from frontend human-readable names to database identifiers
    crypto_name_mapping = {
        'bitcoin': 'BTC',
        'ethereum': 'ETH',
        'solana': 'SOL',
        'matic-network': 'MATIC'
    }

    db_identifier = crypto_name_mapping.get(crypto_name.lower())
    
    if not db_identifier:
        return jsonify({'error': f"No mapping found for {crypto_name}"}), 404
    print(f"db_identifier {db_identifier}")
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['crypto-terminal']
    print("MongoDB Connection Successful")
    collection = db['ai_training_data']
    # Calculate 30 days ago date
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d')  # Adjust format as needed

    try:
        # Fetch data for the last 30 days
        query = {"crypto": db_identifier, "date": {"$gte": thirty_days_ago_str}}
        data = pd.DataFrame(list(collection.find(query).sort("date", -1)))
        
        if data.empty:
            return jsonify({'error': 'No data found'}), 404
        # Prepare data for ARIMA
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data.sort_index(inplace=True)
        
        # Call the prediction function
        forecast = predict_price(data)
        return jsonify({'message': 'Forecast generated successfully', 'forecast': forecast})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        client.close()

def predict_price(data):
    try:
        # Ensure 'close_price' column is a float and not string or object
        data['close_price'] = data['close_price'].astype(float)

        # Create and fit the ARIMA model
        model = ARIMA(data['close_price'], order=(5,1,0))
        model_fit = model.fit()  # 'disp=0' is no longer needed; 'disp' parameter has been removed
        forecast_result = model_fit.forecast(steps=7)  # Forecast for the next 7 days

        # The forecast_result is an array, directly convert it to list
        forecast = list(forecast_result)  # Use list() to convert array to list
        return forecast
    except Exception as e:
        return {'error': str(e)}  # Return error message if forecasting fails

def get_recent_month_data(crypto_id):
    # Mapping crypto_id to its corresponding CSV file
    print(f"{crypto_id}")
    crypto_file_mapping = {
        'bitcoin': 'btc_yearly_extract_exchange_data.csv',
        'ethereum': 'eth_yearly_extract_exchange_data.csv',
        'solana': 'sol_yearly_extract_exchange_data.csv',
        'matic-network': 'matic_yearly_extract_exchange_data.csv',
        'ripple': 'xrp_yearly_extract_exchange_data.csv'
    }
    
    filename = crypto_file_mapping.get(crypto_id.lower())
    print(f"{filename}")
    if not filename:
        return None

    # Adjust the path to go up one directory and then into the 'data' directory
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)

    # Normalize the path to resolve any ".."
    file_path = os.path.normpath(file_path)
    print(f"{file_path}")
    if not os.path.exists(file_path):
        return None
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Assuming there's a 'date' column in your CSV
    df['date'] = pd.to_datetime(df['date'])
    
    # Find the most recent month and year in the data
    most_recent_year = df['date'].dt.year.max()
    most_recent_month = df[df['date'].dt.year == most_recent_year]['date'].dt.month.max()
       
    # Filter the DataFrame for rows from the most recent month
    recent_month_data = df[(df['date'].dt.year == most_recent_year) & (df['date'].dt.month == most_recent_month)]
    
    # Convert the filtered DataFrame to a list of dictionaries for JSON response
    data_list = recent_month_data.to_dict('records')
        
    return data_list

@app.route('/crypto-data/<crypto_id>', methods=['GET'])
def crypto_data(crypto_id):
    data = get_recent_month_data(crypto_id)
    print(f"{data}")
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"error": "Data not found for the specified cryptocurrency"}), 404

def get_current_price(crypto_id):
    # Initialize the CoinGecko API client
    cg = CoinGeckoAPI()

    # Fetch current data for the specified cryptocurrency
    crypto_data = cg.get_coin_by_id(id=crypto_id)

    # Extract price, market cap, and volume in USD
    price_usd = crypto_data['market_data']['current_price']['usd']
    market_cap_usd = crypto_data['market_data']['market_cap']['usd']
    volume_usd = crypto_data['market_data']['total_volume']['usd']

    # Return the data as a dictionary
    return {
        "current_price_usd": price_usd,
        "market_cap_usd": market_cap_usd,
        "24h_volume_usd": volume_usd
    }

@app.route('/crypto-price/<crypto_id>', methods=['GET'])
def crypto_price_endpoint(crypto_id):
    try:
        crypto_data = get_current_price(crypto_id)
        return jsonify(crypto_data), 200
    except Exception as e:
        # In case of error (e.g., invalid crypto_id), return an error message
        return jsonify({"error": "Failed to fetch data", "message": str(e)}), 400

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    return embeddings

@app.route("/search", methods=['POST'])
def semantic_search():
    # Extract the query from the POST request's JSON body
    data = request.get_json(force=True)
    query = data.get('query', '')
    print(query)
    # Convert query to embedding
    query_embedding = get_embedding(query)
    
    # Convert the NumPy array to a Python list
    query_embedding_list = query_embedding.tolist()
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(dbname="semantic", user="postgres", password="postgres", host="localhost")
    cur = conn.cursor()
    
    # Prepare your SQL query. This example uses L2 norm for simplicity.
    sql = """
    SELECT id, instruction, input, output, vector,
    (SELECT sqrt(sum(power(vector[series.idx] - unnested.query_element, 2))) 
    FROM generate_series(1, array_length(vector, 1)) AS series(idx),
        unnest(%s::float[]) WITH ORDINALITY AS unnested(query_element, idx)
    WHERE series.idx = unnested.idx) AS distance
    FROM tweet_sentiments
    ORDER BY distance ASC
    LIMIT 5;
    """
    
    # Execute the query with the query vector
    cur.execute(sql, (query_embedding_list,))
    
    # Fetch results
    results = cur.fetchall()
    # Instead of printing results, store them in a list and return it
    fetched_results = []
    for row in results:
        #fetched_results.append(f"ID: {row[0]}, Instruction: {row[1]}, Input: {row[2]}, Output: {row[3]}, Distance: {row[5]}")
        fetched_results.append(f"Input: {row[2]}, Output: {row[3]}")
    # Return the list of results
    print(fetched_results)
    return fetched_results

@app.route('/predict-close-price', methods=['POST'])
def predict_close_price():
    # Extract data from request
    data = request.get_json()
    df = pd.DataFrame(data)
    
    # Assuming 'open_price' and 'close_price' are in the DataFrame
    X = df[['open_price']].values  # Features
    y = df['close_price'].values  # Target variable

    # Splitting not needed if we are predicting for new/future data
    # Train the model on the entire dataset
    model = LinearRegression()
    model.fit(X, y)
    

    # Assuming you want to predict the close price for the same dates
    # For new predictions, replace X with new data
    predictions = model.predict(X)

    # Return the predictions
    return jsonify(predictions.tolist())

@app.route('/volatility/<crypto_id>', methods=['GET'])
def get_volatility(crypto_id):
    # Mapping crypto_id to its corresponding CSV file
    crypto_file_mapping = {
        'bitcoin': 'btc_yearly_extract_exchange_data.csv',
        'ethereum': 'eth_yearly_extract_exchange_data.csv',
        'solana': 'sol_yearly_extract_exchange_data.csv',
        'matic-network': 'matic_yearly_extract_exchange_data.csv',
        'ripple': 'xrp_yearly_extract_exchange_data.csv'
    }
    
    filename = crypto_file_mapping.get(crypto_id.lower())
    if not filename:
        return jsonify({'error': 'Unsupported cryptocurrency ID'}), 404

    file_path = os.path.join(os.path.dirname(__file__), '..','data', filename)
    if not os.path.exists(file_path):
        return jsonify({'error': 'Data file not found'}), 404
    
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Calculate daily returns
    df['close_price'] = df['close_price'].astype(float)  # Ensure close_price is float
    df['daily_return'] = df['close_price'].pct_change()

    # Calculate volatility as the standard deviation of daily returns
    volatility = df['daily_return'].std()

    return jsonify({'crypto_id': crypto_id, 'volatility_index': volatility})



@app.route('/smart-contract-explorer', methods=['GET'])
def find_new_contracts():
    # Connect to an Ethereum node via Infura
    infura_url = 'https://eth-sepolia.g.alchemy.com/v2/L0FSdySSJYDRRtmTeYDNYPZuiKagkK2d' #os.getenv('SEPOLIA_ALCHEMY_URL') #'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
    print('Web3 URL ${infura_url}')
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Check connection
    if web3.is_connected():
        print("Connected to Ethereum blockchain!")
    else:
        print("Failed to connect.")
        
    latest = web3.eth.block_number
    from_block = latest - 100
    to_block = latest
            
    print(f"Searching for new contracts from block {from_block} to block {to_block}")
    for i in range(from_block, to_block + 1):
        block = web3.eth.get_block(i, full_transactions=True)
        if block is not None:
            transactions = block.transactions
            for tx in transactions:
                if tx.to is None:  # 'to' is None implies contract creation
                    receipt = web3.eth.get_transaction(tx.hash)
                    print(f"\n\nNew contract created at address: {receipt} in block {i}")

    # Example usage
    #latest = web3.eth.blockNumber
    #find_new_contracts(latest - 100, latest)  # Last 100 blocks

        
if __name__ == '__main__':
    app.run(debug=True, port=5005)
