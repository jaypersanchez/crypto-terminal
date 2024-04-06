from flask import Flask, jsonify
from pycoingecko import CoinGeckoAPI
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
