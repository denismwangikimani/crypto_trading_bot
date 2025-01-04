from binance.spot import Spot
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

print(api_key, api_secret)

client = Spot(api_key, api_secret, base_url="https://testnet.binance.vision")

# Function to get the status
def query_binance_status():
    status = Spot().system_status()
    if status["status"] == 0:
        return True
    else:
        raise ConnectionError

# Function to query account
def query_account(api_key, secret_key):
    return Spot(
        api_key=api_key,
        api_secret=secret_key,
        base_url="https://testnet.binance.vision",
    ).account()

# Function to check if account is ready to use
def is_account_ready(api_key, secret_key):
    try:
        account_info = query_account(api_key, secret_key)
        if 'balances' in account_info:
            print("Account is ready to use.")
            return True
        else:
            print("Account is not ready to use.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

# Check if account is ready to use
if is_account_ready(api_key, api_secret):
    print("Proceed with trading operations.")
else:
    print("Please check your API key, secret, and permissions.")

# query testnet
def query_testnet():
    client = Spot(base_url="https://testnet.binance.vision")
    print(client.time())