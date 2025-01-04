import numpy as np
import pandas as pd
from indicator import calculate_indicators
from strategy import strategy

def backtest(data):
    """
    Backtests the strategy using historical price data.
    :param data: Pandas DataFrame containing price data with indicators calculated.
    :return: DataFrame with backtesting results.
    """
    # Calculate indicators
    calculate_indicators(data)
    
    # Generate buy and sell signals
    buy, sell = strategy(data)
    
    # Add signals to DataFrame
    data['buy'] = buy
    data['sell'] = sell
    
    # Simulate trading positions
    data['position'] = np.nan
    data.loc[buy, 'position'] = 1
    data.loc[sell, 'position'] = 0
    data['position'] = data['position'].ffill()  # Forward fill NaN values
    data['position'] = data['position'].fillna(0)  # Fill remaining NaN with 0
    
    # Calculate returns
    data['returns'] = np.log(data['close'] / data['close'].shift(1))
    data['strategy'] = data['position'].shift(1) * data['returns']
    
    # Calculate cumulative returns
    data['cumulative_returns'] = data['strategy'].cumsum().apply(np.exp)
    
    return data

# Example usage
if __name__ == "__main__":
    # Assume `download_historical_data.py` fetched data
    from download_historical_data import download_data
    
    symbol = "BTCUSDT"
    interval = "5m"
    start_str = "1 Jan, 2025"
    historical_data = download_data(symbol, interval, start_str)
    
    # Backtest the strategy
    results = backtest(historical_data)
    print(results[['close', 'buy', 'sell', 'position', 'cumulative_returns']].tail())
