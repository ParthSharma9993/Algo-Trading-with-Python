import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit dropdown
symbol = st.selectbox(
    "Choose a symbol",
    ["AAPL", "GOOGL", "AMZN", "MSFT"]
)

# Load feature data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "data", f"{symbol}_features.csv")
)

df = pd.read_csv(file_path, index_col=0, parse_dates=True)

# Price + SMAs + Bollinger Bands
st.subheader(f"Price with SMAs & Bollinger Bands")
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df.index, df['Close'], label='Close', color='black')
ax.plot(df.index, df['SMA_20'], label='SMA 20', color='blue')
ax.plot(df.index, df['SMA_50'], label='SMA 50', color='orange')
ax.fill_between(df.index, df['bollinger_upper'], df['bollinger_lower'], color='grey', alpha=0.2, label='Bollinger Bands')
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.legend()
st.pyplot(fig)

# MACD
st.subheader(f"MACD")
fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(df.index, df['MACD'], label='MACD', color='green')
ax.plot(df.index, df['MACD_signal'], label='Signal', color='red')
ax.bar(df.index, df['MACD_hist'], label='Hist', color='grey', alpha=0.5)
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.legend()
st.pyplot(fig)

# RSI
st.subheader(f"RSI 14")
fig, ax = plt.subplots(figsize=(14, 3))
ax.plot(df.index, df['RSI_14'], label='RSI 14', color='purple')
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.legend()
st.pyplot(fig)
