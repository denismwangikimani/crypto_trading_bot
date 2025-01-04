'''
Here, we first calculate the SMA using a 50-day window by taking the rolling mean of the close price. 
We then calculate the RSI by first calculating the price changes (delta), and then calculating the average gain and loss over a 14-day window. 
We then calculate the relative strength (rs) as the ratio of the average gain to the average loss, and use this value to calculate the RSI.
'''

# Calculate Technical Indicators
def  calculate_indicators(df):
	# Simple Moving Average (SMA)
	sma = df['close'].rolling(window=50).mean()
	df['SMA'] = sma

	# Relative Strength Index (RSI)
	delta = df['close'].diff()
	gain = delta.where(delta > 0, 0)
	loss = -delta.where(delta < 0, 0)
	avg_gain = gain.rolling(window=14).mean()
	avg_loss = loss.rolling(window=14).mean()
	rs = avg_gain / avg_loss
	rsi = 100 - (100 / (1 + rs))
	df['RSI'] = rsi
    
	return df