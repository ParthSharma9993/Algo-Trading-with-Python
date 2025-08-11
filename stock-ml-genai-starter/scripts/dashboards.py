import os
import pandas as pd
import streamlit as st
from glob import glob

# --- Config ---
LOG_FOLDER = "trade_logs"
st.set_page_config(page_title="📊 Live Trading Dashboard", layout="wide")

st.title("📊 Live Trading Dashboard")

# --- Load all trade logs
log_files = sorted(glob(f"{LOG_FOLDER}/*.txt"))
df_list = []

for file in log_files:
    try:
        df = pd.read_csv(file, names=["time", "symbol", "price", "action", "qty", "stop_price", "pnl"])
        df["time"] = pd.to_datetime(df["time"])
        df_list.append(df)
    except Exception as e:
        st.warning(f"Failed to load {file}: {e}")

if df_list:
    df_all = pd.concat(df_list).sort_values("time")
else:
    st.warning("No trade logs found yet.")
    st.stop()

# --- Show latest trades
st.subheader("Recent Trades")
st.dataframe(df_all.tail(10), use_container_width=True)

# --- Compute cumulative PnL
df_all["cum_pnl"] = df_all["pnl"].cumsum()

col1, col2 = st.columns(2)

with col1:
    st.metric("📈 Total Trades", len(df_all))
    st.metric("💰 Current Unrealized PnL", f"${df_all['pnl'].iloc[-1]:.2f}")

with col2:
    # PnL chart
    st.subheader("📊 Cumulative PnL")
    st.line_chart(df_all.set_index("time")["cum_pnl"])

# --- Auto-refresh every 10 seconds
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 seconds
count = st_autorefresh(interval=5000, key="refresh")
