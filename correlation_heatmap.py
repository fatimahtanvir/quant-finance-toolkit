import pandas as pd
 import numpy as np
 import yfinance as yf
 import matplotlib.pyplot as plt
 import seaborn as sns
 from datetime import datetime

 # 1. Data Acquisition
 def get_data(tickers, start_date, end_date):
  """
  Fetches data for multiple tickers from Yahoo Finance.
  """
  data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
  data.dropna(how='all', inplace=True) #Remove rows where all values are NaN
  return data

 # 2. Calculate Rolling Correlations
 def calculate_rolling_corr(data, window=20):
  """
  Calculates the rolling correlation matrix.
  """
  log_returns = np.log(data).diff().dropna()
  return log_returns.rolling(window=window).corr()

 # 3. Plotting the Heatmap
 def plot_heatmap(corr_data, timestamp=None, ax=None):
  """
  Plots a heatmap of the correlation matrix.
  """
  if ax is None:
  fig, ax = plt.subplots(figsize=(12, 10))
  sns.heatmap(corr_data, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f", ax=ax)
  title = f"Rolling Correlation Matrix"
  if timestamp:
  title += f" at {timestamp}"
  ax.set_title(title)
  return ax

 # 4. Annotate Regimes (Example)
 def annotate_regime(ax, timestamp, text):
  """
  Annotates a specific regime on the heatmap.
  """
  ax.text(0.5, -0.1, text, size=12, ha="center", transform=ax.transAxes, color="white",
  bbox=dict(facecolor="red", alpha=0.7))

 # 5. Main Execution
 if __name__ == '__main__':
  # Define asset tickers
  tickers = ['SPY', # S&P 500 ETF (Equity Index)
  'EURUSD=X', # EUR/USD (FX)
  'GC=F', # Gold Futures (Commodity)
  'CL=F', # Crude Oil Futures (Commodity)
  'ZB=F'] # US Treasury Bond Futures (Rates)

  start_date = '2022-01-01'
  end_date = '2024-01-01'
  window = 60 # Rolling window size

  # Fetch data
  data = get_data(tickers, start_date, end_date)

  if data is not None and not data.empty:
  # Calculate rolling correlations
  rolling_corr = calculate_rolling_corr(data, window=window)

  # Select a specific timestamp for the heatmap (e.g., a stress period)
  timestamp = '2023-03-15'
  corr_at_timestamp = rolling_corr.loc[timestamp]

  # Plot the heatmap
  ax = plot_heatmap(corr_at_timestamp, timestamp=timestamp)

  # Annotate a regime (example)
  annotate_regime(ax, timestamp, "Potential Risk-Off Period (e.g., Banking Concerns)")

  plt.tight_layout()
  plt.show()

  #Example: Plotting a series of heatmaps over time
  # fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(18, 15))
  # axes = axes.flatten()
  # num_plots = len(axes)
  # dates = rolling_corr.index[::len(rolling_corr) // num_plots][:num_plots]

  # for i, date in enumerate(dates):
  # corr_data = rolling_corr.loc[date]
  # ax = axes[i]
  # plot_heatmap(corr_data, timestamp=date.strftime('%Y-%m-%d'), ax=ax)
  # ax.set_title(date.strftime('%Y-%m-%d'))

  # plt.tight_layout()
  # plt.show()
  else:
  print("No data retrieved. Check tickers and date range.")
