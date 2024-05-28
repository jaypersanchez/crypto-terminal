from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/yKN3oudM7COVTUQ6VeyS5XrmXHGzswcv'))  # Replace with your Infura endpoint
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Address of Uniswap's Router contract
router_address = Web3.toChecksumAddress("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
with open('uniswapv2.abi', 'r') as f:
    _abi = json.load(f) 
uniswap_router = w3.eth.contract(
    address=router_address,
    abi=_abi  # Replace with the ABI of Uniswap Router contract
)

# Example: Call a function on Uniswap's Router contract
pair = uniswap_router.functions.getPair(token1_address, token2_address).call()

# Example: Execute a transaction on Uniswap's Router contract
tx_hash = uniswap_router.functions.swapExactETHForTokens(
    amountOutMin,
    [WETH_ADDRESS, token_address],
    recipient_address,
    deadline
).transact({'from': sender_address, 'value': amount_in_wei})
