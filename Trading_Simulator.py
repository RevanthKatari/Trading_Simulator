import pandas as pd
import numpy as np

# Load historical market data (replace 'your_dataset.csv' with your data file)
df = pd.read_csv(path)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Define parameters for the strategy
short_window = 50  # Short-term SMA window
long_window = 200  # Long-term SMA window
stop_loss_percent = 5  # Set your desired stop-loss percentage (e.g., 5%)

# Calculate the short-term and long-term SMAs
df['SMA_Short'] = df['Close'].rolling(window=short_window).mean()
df['SMA_Long'] = df['Close'].rolling(window=long_window).mean()

# Create signals based on crossover
df['Signal'] = 0  # Initialize signal column with 0 (no action)
df['Signal'][short_window:] = np.where(df['SMA_Short'][short_window:] > df['SMA_Long'][short_window:], 1, 0)

# Implement stop-loss orders
position = 0  # Initialize position as 0 (no position)
for index, row in df.iterrows():
    if row['Signal'] == 1:
        # Buy signal, go long
        position = 1
        entry_price = row['Close']
        stop_loss_price = entry_price - (entry_price * stop_loss_percent / 100)
    elif row['Signal'] == 0 and position == 1:
        # If not in a buy signal and in a long position, check stop-loss
        if row['Low'] <= stop_loss_price:
            # Execute stop-loss, sell position
            position = 0
            stop_loss_triggered = True
        else:
            # Continue holding position
            continue

# Calculate daily returns
df['Daily_Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(1)

# Calculate cumulative returns
df['Cumulative_Return'] = (1 + df['Strategy_Return']).cumprod()

# Print the performance metrics
total_trades = df['Signal'].sum()
winning_trades = (df['Strategy_Return'] > 0).sum()
losing_trades = (df['Strategy_Return'] < 0).sum()
win_rate = (winning_trades / total_trades) * 100
cumulative_return = (df['Cumulative_Return'][-1] - 1) * 100

print(f"Total Trades: {total_trades}")
print(f"Winning Trades: {winning_trades}")
print(f"Losing Trades: {losing_trades}")
print(f"Win Rate: {win_rate:.2f}%")
print(f"Cumulative Return: {cumulative_return:.2f}%")

# Optionally, you can visualize the cumulative return
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Cumulative_Return'], label='Strategy Cumulative Return', color='b')
plt.plot(df.index, (1 + df['Daily_Return']).cumprod(), label='Market Cumulative Return', color='g')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.title('Strategy vs. Market Cumulative Return')
plt.grid(True)
plt.show()
