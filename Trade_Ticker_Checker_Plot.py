import pandas as pd
import matplotlib.pyplot as plt

mkt_ticker = input("please enter the stock ticker: ")

path = "/content/data/"+ mkt_ticker + ".csv"
df = pd.read_csv(path)
df.head(5)   # General check


missing_values = df.isnull().sum()      # Check for missing values

df.fillna(method='ffill', inplace=True)   # Handle missing values (e.g., forward fill)


df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by='Date', inplace=True)

df['MA_20'] = df['Close'].rolling(window=20).mean()   # Calculate 20-day moving average

df.drop(['Series', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble'], axis=1, inplace=True)  # Drop columns that are not needed
 
df.drop_duplicates(inplace=True)   # Remove duplicate rows

df.set_index('Date', inplace=True)   # Set 'Date' as the index
df.plot() # General Plot
