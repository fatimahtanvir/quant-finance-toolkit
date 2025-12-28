import pandas as pd
 import numpy as np
 import yfinance as yf
 from datetime import datetime, timedelta
 import matplotlib.pyplot as plt

 # 1. Data Acquisition
 def get_stock_data(ticker, start_date, end_date):
  """
  Fetches stock data from Yahoo Finance and calculates log returns.
  """
  try:
  data = yf.download(ticker, start=start_date, end=end_date)
  if data.empty:
  raise ValueError(f"No data found for ticker {ticker} within the specified date range.")
  data['Log Returns'] = np.log(data['Close'] / data['Close'].shift(1))
  data.dropna(inplace=True)
  return data
  except Exception as e:
  print(f"Error fetching data for {ticker}: {e}")
  return None

 # 2. Event Definition and Windowing
 def define_event_window(event_date, window_before=5, window_after=5):
  """
  Defines the event window around a specific date.
  """
  event_date = pd.to_datetime(event_date)
  before_start = event_date - timedelta(days=window_before)
  after_end = event_date + timedelta(days=window_after)
  return before_start, after_end, event_date

 # 3. Metric Calculation
 def calculate_metrics(data, before_start, event_date, after_end):
  """
  Calculates returns, volatility changes, and drawdowns within the event window.
  """
  try:
  # Slice data into before and after event
  before_data = data[(data.index >= before_start) & (data.index < event_date)]
  after_data = data[(data.index >= event_date) & (data.index <= after_end)]

  if before_data.empty or after_data.empty:
  raise ValueError("Not enough data before or after the event.")

  # Returns
  before_cumulative_return = np.exp(before_data['Log Returns'].sum()) - 1
  after_cumulative_return = np.exp(after_data['Log Returns'].sum()) - 1

  # Volatility
  before_volatility = before_data['Log Returns'].std() * np.sqrt(252)
  after_volatility = after_data['Log Returns'].std() * np.sqrt(252)

  # Drawdown (simplified - from peak to trough within the window)
  before_cumulative_returns = np.exp(before_data['Log Returns'].cumsum())
  after_cumulative_returns = np.exp(after_data['Log Returns'].cumsum())

  before_drawdown = (before_cumulative_returns / before_cumulative_returns.cummax() - 1).min()
  after_drawdown = (after_cumulative_returns / after_cumulative_returns.cummax() - 1).min()

  return {
  'before_return': before_cumulative_return,
  'after_return': after_cumulative_return,
  'before_volatility': before_volatility,
  'after_volatility': after_volatility,
  'before_drawdown': before_drawdown,
  'after_drawdown': after_drawdown
  }

  except Exception as e:
  print(f"Error calculating metrics: {e}")
  return None

 # 4. Cross-Asset Comparison
 def compare_assets(results):
  """
  Compares the event impact across different assets.
  """
  df = pd.DataFrame(results).T # Transpose for easier comparison
  print(df)
  #Add more sophisticated comparison logic here (e.g., sorting, ranking)
  return df

 # 5. Main Execution
 if __name__ == '__main__':
  # Define assets and event
  assets = {
  'SPY': 'S&P 500 ETF',
  'EURUSD=X': 'EUR/USD',
  'GC=F': 'Gold Futures'
  }
  event_date = '2023-03-14' # Example: CPI Release Date
  window_before = 5
  window_after = 5

  results = {}
  start_date = '2023-01-01'
  end_date = '2023-04-01'

  # Analyze each asset
  for ticker, name in assets.items():
  print(f"Analyzing {name} ({ticker})...")
  data = get_stock_data(ticker, start_date, end_date)
  if data is not None:
  before_start, after_end, event_date = define_event_window(event_date, window_before, window_after)
  metrics = calculate_metrics(data, before_start, event_date, after_end)
  if metrics:
  results[name] = metrics
  else:
  print(f"Skipping {name} due to insufficient data.")
  else:
  print(f"Could not retrieve data for {name} ({ticker}).")

  # Compare assets
  if results:
  comparison_df = compare_assets(results)

  #Example: Plotting Returns
  # comparison_df[['before_return', 'after_return']].plot(kind='bar', figsize=(10,6))
  # plt.title('Returns Before and After Event')
  # plt.ylabel('Return')
  # plt.xticks(rotation=45)
  # plt.tight_layout()
  # plt.show()
  else:
  print("No results to compare.")
