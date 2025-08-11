import os
import time
import pandas as pd
import joblib
import datetime as dt
from pathlib import Path

# === Settings ===
SYMBOLS = ["AAPL", "GOOGL", "AMZN", "MSFT"]  # symbols you have data for
MODEL_PATH = "models/my_model.pkl"
DATA_FOLDER = "data"
TRADE_LOG_FOLDER = "trade_logs"
POSITION_FILE = "trade_logs/positions.csv"  # to track open positions
SLEEP_SECONDS = 60  # loop every minute
POSITION_SIZE = 10  # number of shares per trade

# === Prepare folders ===
Path(TRADE_LOG_FOLDER).mkdir(exist_ok=True)

# === Load model once ===
model = joblib.load(MODEL_PATH)

# === Initialize PnL ===
realized_pnl = 0
positions = {}  # symbol -> {'entry_price': float, 'qty': int}

# === Restore previous positions if exist ===
if os.path.exists(POSITION_FILE):
    df_pos = pd.read_csv(POSITION_FILE, index_col=0)
    for sym, row in df_pos.iterrows():
        positions[sym] = {"entry_price": row['entry_price'], "qty": row['qty']}
    print(f"Restored positions: {positions}")

# === Start live loop ===
while True:
    for symbol in SYMBOLS:
        try:
            # 1️⃣ Load latest data
            df = pd.read_csv(f"{DATA_FOLDER}/{symbol}_1min.csv", index_col=0, parse_dates=True)
            
            # 2️⃣ Compute features (replace with your actual feature logic)
            df["returns"] = df["Close"].pct_change()
            df["ma_5"] = df["Close"].rolling(5).mean()
            df["ma_20"] = df["Close"].rolling(20).mean()

            # 3️⃣ Take latest row's features
            last_row = df.iloc[-1:]
            features = last_row[["returns", "ma_5", "ma_20"]].fillna(0)

            # 4️⃣ Predict
            prob = model.predict_proba(features)[0]
            will_go_up = prob[1] > 0.5
            price = last_row["Close"].values[0]

            # 5️⃣ Decide action
            action = "BUY" if will_go_up else "SELL"
            qty = POSITION_SIZE
            now = dt.datetime.utcnow().isoformat()

            decision = ""
            if action == "BUY":
                # open or update position
                positions[symbol] = {"entry_price": price, "qty": qty}
                decision = "✅ BUY"
            else:
                if symbol in positions:
                    # close position & compute realized PnL
                    entry = positions.pop(symbol)
                    trade_pnl = (price - entry["entry_price"]) * entry["qty"]
                    realized_pnl += trade_pnl
                    decision = f"❌ SELL, realized PnL: {trade_pnl:.2f}"
                else:
                    decision = "❌ SELL, no open position"

            # 6️⃣ Log trade
            log_line = f"{now},{symbol},{price:.2f},{action},{qty},{realized_pnl:.2f},{prob[1]:.2f}\n"
            log_file = f"{TRADE_LOG_FOLDER}/trades_{dt.date.today()}.txt"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_line)

            print(f"{now} | {symbol} | {action} @ {price:.2f} | {decision} | Total PnL: {realized_pnl:.2f}")

        except Exception as e:
            print(f"Error with {symbol}: {e}")

    # 7️⃣ Save positions to CSV (dashboard can read)
    if positions:
        df_pos = pd.DataFrame.from_dict(positions, orient='index')
        df_pos.to_csv(POSITION_FILE)
    else:
        if os.path.exists(POSITION_FILE):
            os.remove(POSITION_FILE)

    # 8️⃣ Sleep before next loop
    time.sleep(10)
