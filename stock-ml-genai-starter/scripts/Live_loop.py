import os
import time
import pandas as pd
import joblib
from datetime import datetime

# --- Config ---
symbol = 'AAPL'
capital = 10_000
risk_per_trade = 0.01
stop_loss_pct = 0.005
features = ['Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist']

model_path = 'models/price_direction_rf.pkl'
data_path = f'data/{symbol}_features.csv'
log_folder = 'trade_logs'

# Create log folder if missing
os.makedirs(log_folder, exist_ok=True)

# Load model once
model = joblib.load(model_path)
print(f"✅ Loaded model: {model_path}")

# --- Initialize positions list
positions = []   # Each: {'entry_price': float, 'qty': int, 'action': 'BUY'/'SELL'}

# --- Live loop ---
while True:
    try:
        print(f"\n=== {datetime.now()} | Predicting for {symbol} ===")

        # Load latest data
        df = pd.read_csv(data_path, index_col=0, parse_dates=True)
        latest = df.iloc[-1:]
        current_price = latest['Close'].values[0]

        # Predict
        pred = model.predict(latest[features])[0]
        proba = model.predict_proba(latest[features])[0]

        # Position sizing
        dollar_risk = capital * risk_per_trade
        stop_loss_amount = current_price * stop_loss_pct
        qty = max(int(dollar_risk / stop_loss_amount), 1)

        # Decide action
        if pred == 1 and proba[1] > 0.6:
            action = "BUY"
            stop_price = current_price * (1 - stop_loss_pct)
        elif pred == 0 and proba[0] > 0.6:
            action = "SELL"
            stop_price = current_price * (1 + stop_loss_pct)
        else:
            action = "HOLD"
            stop_price = None

        # --- Record new position if BUY or SELL
        if action in ["BUY", "SELL"]:
            positions.append({
                'entry_price': current_price,
                'qty': qty,
                'action': action
            })

        # --- Compute PnL on open positions
        total_pnl = 0
        for pos in positions:
            if pos['action'] == "BUY":
                pnl = (current_price - pos['entry_price']) * pos['qty']
            elif pos['action'] == "SELL":
                pnl = (pos['entry_price'] - current_price) * pos['qty']
            else:
                pnl = 0
            total_pnl += pnl

        # Print info
        print(f"Price: {current_price:.2f} | Pred: {pred} | Prob: {proba}")
        print(f"Action: {action} | Qty: {qty} | Stop Loss: {stop_price:.2f}" if stop_price else f"Action: {action}")
        print(f"📊 Current Unrealized PnL: ${total_pnl:.2f} across {len(positions)} open positions")

        # Log to file
        log_filename = datetime.now().strftime(f"{log_folder}/trades_%Y-%m-%d.txt")
        log_entry = f"{datetime.now()}, {symbol}, {current_price:.2f}, {action}, {qty}, {stop_price}, {total_pnl:.2f}\n"
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(log_entry)

    except Exception as e:
        print(f"⚠️ Error: {e}")

    time.sleep(5)  # wait 5 seconds before next iteration
