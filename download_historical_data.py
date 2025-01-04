import pandas as pd
import time
from binance.spot import Spot
from binance_connect import client

def convert_to_milliseconds(date_str):
    """
    Converts a date string to milliseconds since the Unix epoch, handling multiple formats.
    """
    from datetime import datetime
    for fmt in ("%d %b, %Y", "%d %b %Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized: {date_str}")


def download_data(symbol, interval, start_str):
    """
    Downloads historical price data using the Binance Spot API.
    :param symbol: Trading pair symbol (e.g., 'BTCUSDT').
    :param interval: Time interval for the data (e.g., '1d', '1h').
    :param start_str: Start time in string format (e.g., '1 Jan, 2022').
    :return: Pandas DataFrame with historical data.
    """
    print(f"Downloading data for {symbol}. Interval: {interval}. Starting from: {start_str}")

    # Convert start date to milliseconds
    start_time = convert_to_milliseconds(start_str)
    all_data = []
    while True:
        klines = client.klines(symbol=symbol, interval=interval, startTime=start_time)
        if not klines:
            break
        all_data.extend(klines)
        start_time = klines[-1][6] + 1  # Move to the next batch
        time.sleep(1)  # Avoid rate limiting

    # Convert to DataFrame
    data = pd.DataFrame(
        all_data,
        columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'number_of_trades', 
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ]
    )
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data['close'] = data['close'].astype(float)
    return data

# Example usage
if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = "5m"
    start_str = "1 Jan, 2025"
    historical_data = download_data(symbol, interval, start_str)
    print(historical_data.head())
