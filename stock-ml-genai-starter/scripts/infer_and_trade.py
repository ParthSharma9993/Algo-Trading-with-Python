
# For BUY/SELL of AAPL stock based on a pre-trained model
# This script loads the model, predicts the price direction, and decides on a trade action
import pandas as pd
import os
import joblib
from datetime import datetime

# Settings
symbol = 'AAPL'
capital = 10_000          # total capital
risk_per_trade = 0.01     # risk 1% per trade
stop_loss_pct = 0.005     # stop loss 0.5%

# --- Load latest data
df = pd.read_csv(f"data/{symbol}_features.csv", index_col=0, parse_dates=True)
latest = df.iloc[-1:]
current_price = latest['Close'].values[0]

# --- Load model & predict
model = joblib.load('models/price_direction_rf.pkl')
features = ['Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist']
pred = model.predict(latest[features])[0]
proba = model.predict_proba(latest[features])[0]

# --- Decide position size
dollar_risk = capital * risk_per_trade   # e.g. $100 risk per trade
stop_loss_amount = current_price * stop_loss_pct
qty = max(int(dollar_risk / stop_loss_amount), 1)

# --- Decide action
if pred == 1 and proba[1] > 0.6:
    action = "BUY"
    stop_price = current_price * (1 - stop_loss_pct)
elif pred == 0 and proba[0] > 0.6:
    action = "SELL"
    stop_price = current_price * (1 + stop_loss_pct)
else:
    action = "HOLD"
    stop_price = None

# --- Print summary
print(f"\n=== {datetime.now()} ===")
print(f"Symbol: {symbol}")
print(f"Price: {current_price:.2f}")
print(f"Pred: {pred} Prob: {proba}")
print(f"Action: {action} | Qty: {qty} | Stop Loss: {stop_price:.2f}" if stop_price else f"Action: {action}")

# --- Log to file

# Make sure the folder exists
os.makedirs('trade_logs', exist_ok=True)

# Build log filename per day
log_filename = datetime.now().strftime("trade_logs/trades_%Y-%m-%d.txt")

log_entry = f"{datetime.now()}, {symbol}, {current_price:.2f}, {action}, {qty}, {stop_price}\n"

with open(log_filename, "a", encoding="utf-8") as f:
    f.write(log_entry)

print(f"✅ Trade logged to {log_filename}")
