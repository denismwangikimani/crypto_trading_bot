import matplotlib.pyplot as plt
from download_historical_data import download_data
from backtest import backtest

# Step 9: Plot the Results
def plot_results(data):
    """
    Plot the cumulative returns to visualize the performance of the strategy.

    Args:
        data (DataFrame): DataFrame containing the 'cumulative_returns' column.
    """
    data[['cumulative_returns']].plot(figsize=(10, 6), legend=True)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.title('Backtesting Results')
    plt.grid()
    plt.show()

# Step 10: Run the crypto Bot in Test Mode
def test_trading():
    """
    Run the backtesting process for the trading strategy.

    Returns:
        DataFrame: Backtested data with cumulative returns.
    """
    # Download historical data for BTC/USDT with a 5-minute interval starting from Jan 1, 2022
    print("Downloading historical data...")
    data = download_data('BTCUSDT', '1m', '1 Jan, 2025')


    # Run the backtest on the downloaded data
    print("Running backtest...")
    data = backtest(data)

    # Plot the results of the backtest
    print("Plotting results...")
    plot_results(data)

    return data

# Run the test trading process when executing the script
if __name__ == "__main__":
    test_trading()
