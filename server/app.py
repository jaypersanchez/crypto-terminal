from flask import Flask, jsonify, request
from pycoingecko import CoinGeckoAPI
from flask_cors import CORS
import pandas as pd
import os
import psycopg2
from transformers import AutoTokenizer, AutoModel
import torch

app = Flask(__name__)
CORS(app)
# Initialize the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

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
        
if __name__ == '__main__':
    app.run(debug=True, port=5005)
