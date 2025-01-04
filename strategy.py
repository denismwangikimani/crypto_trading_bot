def strategy(df):
    """
    Define the trading strategy using SMA and RSI indicators.

    Args:
        df (DataFrame): A DataFrame containing 'SMA' and 'RSI' columns.

    Returns:
        tuple: Two boolean Series representing buy and sell signals.
    """
    # Buy signal: SMA is increasing and RSI is below 30
    buy = (df['SMA'] > df['SMA'].shift(1)) & (df['RSI'] < 30)

    # Sell signal: SMA is decreasing or RSI is above 70
    sell = (df['SMA'] < df['SMA'].shift(1)) | (df['RSI'] > 70)

    return buy, sell