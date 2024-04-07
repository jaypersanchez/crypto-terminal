from flask import Flask, jsonify
from pycoingecko import CoinGeckoAPI
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

def get_recent_month_data(crypto_id):
    # Mapping crypto_id to its corresponding CSV file
    print(f"{crypto_id}")
    crypto_file_mapping = {
        'bitcoin': 'btc_yearly_extract_exchange_data.csv',
        'ethereum': 'eth_yearly_extract_exchange_data.csv',
        'solana': 'sol_yearly_extract_exchange_data.csv',
        'matic-network': 'matic_yearly_extract_exchange_data.csv'
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
    
if __name__ == '__main__':
    app.run(debug=True, port=5005)
