import pandas as pd
 import numpy as np
 import yfinance as yf
 from datetime import datetime

 # 1. Data Acquisition & Preparation
 def get_stock_data(ticker, start_date, end_date):
  """
  Fetches stock data from Yahoo Finance.
  """
  try:
  data = yf.download(ticker, start=start_date, end=end_date)
  if data.empty:
  raise ValueError(f"No data found for ticker {ticker} within the specified date range.")
  data['Log Returns'] = np.log(data['Close'] / data['Close'].shift(1))
  data.dropna(inplace=True) # Remove the first row with NaN
  return data
  except Exception as e:
  print(f"Error fetching data for {ticker}: {e}")
  return None

 # 2. Volatility Calculation Functions
 def historical_volatility(log_returns, trading_days=252):
  """
  Calculates annualized historical volatility.
  """
  return np.sqrt(trading_days * np.var(log_returns))

 def rolling_volatility(log_returns, window):
  """
  Calculates rolling window volatility.
  """
  return log_returns.rolling(window=window).std() * np.sqrt(252)

 def ewma_volatility(log_returns, lambda_val=0.94):
  """
  Calculates EWMA volatility.
  """
  return log_returns.ewm(alpha=(1 - lambda_val)).std() * np.sqrt(252)

 # 3. Macro Event Analysis (Illustrative)
 def analyze_macro_event(data, event_date, window_before=20, window_after=20):
  """
  Compares volatility before and after a macro event.
  """
  try:
  event_date = pd.to_datetime(event_date)
  before_start = event_date - pd.Timedelta(days=window_before)
  before_end = event_date - pd.Timedelta(days=1)
  after_start = event_date + pd.Timedelta(days=1)
  after_end = event_date + pd.Timedelta(days=window_after)

  before_data = data[(data.index >= before_start) & (data.index <= before_end)]
  after_data = data[(data.index >= after_start) & (data.index <= after_end)]

  if before_data.empty or after_data.empty:
  raise ValueError("Not enough data before or after the event date.")

  before_volatility = historical_volatility(before_data['Log Returns'])
  after_volatility = historical_volatility(after_data['Log Returns'])

  return before_volatility, after_volatility

  except Exception as e:
  print(f"Error analyzing macro event: {e}")
  return None, None

 # 4. Main Execution
 if __name__ == '__main__':
  ticker = 'AAPL' # Example stock
  start_date = '2022-01-01'
  end_date = '2024-01-01'

  # Fetch data
  stock_data = get_stock_data(ticker, start_date, end_date)

  if stock_data is not None:
  # Calculate and print historical volatility
  hist_vol = historical_volatility(stock_data['Log Returns'])
  print(f"Historical Volatility: {hist_vol:.4f}")

  # Calculate and print rolling volatilities
  rolling_20 = rolling_volatility(stock_data['Log Returns'], window=20)
  rolling_60 = rolling_volatility(stock_data['Log Returns'], window=60)
  rolling_120 = rolling_volatility(stock_data['Log Returns'], window=120)

  print(f"Rolling 20-day Volatility (last value): {rolling_20.iloc[-1]:.4f}")
  print(f"Rolling 60-day Volatility (last value): {rolling_60.iloc[-1]:.4f}")
  print(f"Rolling 120-day Volatility (last value): {rolling_120.iloc[-1]:.4f}")

  # Calculate and print EWMA volatility
  ewma = ewma_volatility(stock_data['Log Returns'])
  print(f"EWMA Volatility (lambda=0.94, last value): {ewma.iloc[-1]:.4f}")

  # Example macro event analysis
  event_date = '2023-03-14' # Example CPI release date
  before_vol, after_vol = analyze_macro_event(stock_data, event_date)

  if before_vol is not None and after_vol is not None:
  print(f"Volatility before {event_date}: {before_vol:.4f}")
  print(f"Volatility after {event_date}: {after_vol:.4f}")
