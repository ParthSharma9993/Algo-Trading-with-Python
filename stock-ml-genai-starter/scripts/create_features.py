import os
import pandas as pd

symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'SPY', 'EURUSD=X', 'GBPUSD=X']

# Make sure 'data' folder exists
os.makedirs('data', exist_ok=True)

for symbol in symbols:
    print(f"\n=== Processing {symbol} ===")

    # Load CSV; parse dates; index = first column
    df = pd.read_csv(f"data/{symbol}_1min.csv", index_col=0, parse_dates=True)

    # Convert price/volume columns to numeric (fix strings issue)
    for col in ['Close', 'Open', 'High', 'Low', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows where Close is NaN (in case parsing failed)
    df.dropna(subset=['Close'], inplace=True)

    # Returns
    df['returns'] = df['Close'].pct_change(fill_method=None)

    # Simple Moving Averages
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # RSI (14)
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # Golden Cross / Death Cross
    df['golden_cross'] = ((df['SMA_20'] > df['SMA_50']) & (df['SMA_20'].shift(1) <= df['SMA_50'].shift(1))).astype(int)
    df['death_cross'] = ((df['SMA_20'] < df['SMA_50']) & (df['SMA_20'].shift(1) >= df['SMA_50'].shift(1))).astype(int)

    # MACD
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_hist'] = df['MACD'] - df['MACD_signal']

    # Bollinger Bands (using SMA_20 and std)
    std = df['Close'].rolling(window=20).std()
    df['bollinger_mid'] = df['SMA_20']
    df['bollinger_upper'] = df['SMA_20'] + 2 * std
    df['bollinger_lower'] = df['SMA_20'] - 2 * std
    df['bollinger_bandwidth'] = df['bollinger_upper'] - df['bollinger_lower']

    # Drop initial NaNs from rolling windows
    df.dropna(inplace=True)

    print(df.head())

    # Save new feature file
    out_file = f"data/{symbol}_features.csv"
    df.to_csv(out_file)
    print(f"✅ Saved features to {out_file}")
