# Load CSV, compute mid price, save clean data
import os
import yfinance as yf

# Make sure 'data' folder exists
os.makedirs('data', exist_ok=True)

symbols = ['AAPL', 'SPY', 'MSFT', 'GOOGL', 'AMZN', 'EURUSD=X', 'GBPUSD=X']

for symbol in symbols:
    print(f"\n=== {symbol} ===")
    df = yf.download(tickers=symbol, interval='1m', period='1d')
    print(df.head())

    df.to_csv(f"data/{symbol}_1min.csv")
    print(f"Saved to data/{symbol}_1min.csv")
