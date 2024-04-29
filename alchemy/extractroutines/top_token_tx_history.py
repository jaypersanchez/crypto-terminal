import datetime
import requests
import json
from alchemy import Alchemy, Network
import time
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_top_token_transactions(network, api_key):
    # Initialize Alchemy
    alchemy = Alchemy(api_key=api_key, network=network)

    # Assuming 'top tokens' means most active or largest by market cap, here we are
    # just hard-coding some common top tokens for demonstration.
    tokens = {
        Network.ETH_MAINNET: ["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",  # WETH
                              "0xdac17f958d2ee523a2206206994597c13d831ec7",  # USDT
                              "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
                              "0x6b175474e89094c44da98b954eedeac495271d0f"], # DAI
        Network.POLYGON_MAINNET: ["0x0000000000000000000000000000000000001010"]  # MATIC itself
    }

    # Prepare dictionary to store all transaction data
    all_transactions = {}

    # Fetch transactions for each token
    for token in tokens.get(network, []):
        txs = alchemy.core.get_asset_transfers(
            from_block='latest-10',  # Adjust range as needed
            to_block='latest',
            contract_addresses=[token]
        )

        # Add transactions to the dictionary under their token address
        all_transactions[token] = txs['transfers']

    # Write transactions to JSON file
    with open('../../data/tx_hashes.json', 'w') as f:
        json.dump(all_transactions, f, indent=4)

    print(f"Transaction data for {network.value} has been saved to ../../data/tx_hashes.json.")


def main():
    # Alchemy API keys - replace with your actual API keys
    api_keys = {
        Network.ETH_MAINNET: os.getenv('ETH_ALCHEMY_URL'),
        Network.POLYGON_MAINNET: os.getenv('MATIC_ALCHEMY_URL')
    }

    # Fetch Ethereum and Polygon transactions
    get_top_token_transactions(Network.ETH_MAINNET, api_keys[Network.ETH_MAINNET])
    get_top_token_transactions(Network.POLYGON_MAINNET, api_keys[Network.POLYGON_MAINNET])

    # Solana and Bitcoin would need separate handling
    # For Solana, use: https://docs.solana.com/developing/clients/jsonrpc-api
    # For Bitcoin, consider Blockstream API: https://blockstream.info/api/

if __name__ == "__main__":
    main()
