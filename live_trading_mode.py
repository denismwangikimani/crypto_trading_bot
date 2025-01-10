import time
from binance.spot import Spot
from download_historical_data import download_data
from indicator import calculate_indicators
from strategy import strategy
from binance_connect import client

def live_trading():
    """
    Executes live trading using the Binance API and a trading strategy.
    """
    # Initialize variables to track previous signals
    prev_buy_signal = False
    prev_sell_signal = False

    while True:
        try:
            # Step 1: Download the latest data
            print("Fetching live data...")
            data = download_data('BTCUSDT', '5m', '10 Jan 2025')
            
            # Step 2: Calculate indicators
            calculate_indicators(data)
            
            # Step 3: Get buy and sell signals
            buy_signal, sell_signal = strategy(data)
            # Get the latest buy and sell signal
            buy_signal = buy_signal.iloc[-1]
            sell_signal = sell_signal.iloc[-1]  


            # Step 4: Execute buy order if buy signal is generated
            if buy_signal and not prev_buy_signal:
                order = client.new_order(
                    symbol='BTCUSDT',
                    side='BUY',
                    type='MARKET',
                    quantity=0.001
                )
                print('Buy signal generated. Placing market buy order:', order)

            # Step 5: Execute sell order if sell signal is generated
            elif sell_signal and not prev_sell_signal:
                order = client.new_order(
                    symbol='BTCUSDT',
                    side='SELL',
                    type='MARKET',
                    quantity=0.001
                )
                print('Sell signal generated. Placing market sell order:', order)

            # Step 6: Update previous signals
            prev_buy_signal = buy_signal
            prev_sell_signal = sell_signal

        except Exception as e:
            print(f"Error during live trading: {e}")

        # Wait before checking again
        time.sleep(60)

if __name__ == "__main__":
    print("Starting live trading...")
    live_trading()
