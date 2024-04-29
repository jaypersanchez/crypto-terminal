import datetime
import requests
import os
import sys
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(filename='blockchain_tx_history.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_blocks_for_date(api_url, date):
    """Assume this function will get block numbers for the start and end of a date"""
    # Placeholder function
    return [12345, 12346]  # Example block numbers

def fetch_transactions_for_blocks(api_url, block_numbers, limit=1000):
    transactions = []
    for block_number in block_numbers:
        if len(transactions) >= limit:
            break
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True]  # True to include transactions
        }
        response = requests.post(api_url, json=payload)
        block_data = response.json()
        transactions.extend(block_data['result']['transactions'])
        if len(transactions) > limit:
            transactions = transactions[:limit]
    return transactions

def date_range():
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=30)
    return start_date, today

def main():
    logging.info("Starting transaction history extraction process...")
    
    eth_url = os.getenv('ETH_ALCHEMY_URL')
    matic_url = os.getenv('MATIC_ALCHEMY_URL')
    start_date, end_date = date_range()
    total_days = (end_date - start_date).days + 1
    processed_days = 0
    start_time = time.time()

    for single_date in (start_date + datetime.timedelta(n) for n in range(total_days)):
        eth_blocks = get_blocks_for_date(eth_url, single_date)
        matic_blocks = get_blocks_for_date(matic_url, single_date)

        eth_transactions = fetch_transactions_for_blocks(eth_url, eth_blocks, 1000)
        matic_transactions = fetch_transactions_for_blocks(matic_url, matic_blocks, 1000)

        logging.info(f"Ethereum transactions for {single_date}: {len(eth_transactions)} transactions fetched")
        logging.info(f"Polygon transactions for {single_date}: {len(matic_transactions)} transactions fetched")
        
        processed_days += 1
        elapsed_time = time.time() - start_time
        rate = processed_days / elapsed_time
        eta = (total_days - processed_days) / rate if rate > 0 else float('inf')
        sys.stdout.write(f"\rProcessed {processed_days} of {total_days} days - Rate: {rate:.2f} days/s, ETA: {eta:.2f} seconds ")
        sys.stdout.flush()

    logging.info("Finished transaction history extraction.")
    sys.stdout.write("\nAll data has been processed.\n")

if __name__ == "__main__":
    main()
