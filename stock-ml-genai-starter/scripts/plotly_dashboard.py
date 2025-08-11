import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Symbols you have
symbols = ['AAPL', 'AMZN', 'GOOGL']  # add more if you want

for symbol in symbols:
    print(f"=== Plotting {symbol} ===")
    df = pd.read_csv(f"data/{symbol}_features.csv", index_col=0, parse_dates=True)
    
    # Use last N rows for clarity
    N = 200
    df = df.iloc[-N:]

    # Create figure with 4 rows: Price, Volume, MACD, RSI
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                        row_heights=[0.5, 0.1, 0.2, 0.2],
                        vertical_spacing=0.02,
                        subplot_titles=(f"{symbol} Candlestick + SMA",
                                        "Volume", "MACD", "RSI"))

    # --- Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                                 open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'],
                                 name='Candles'), row=1, col=1)

    # --- SMA_20 & SMA_50
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='blue'), name='SMA_20'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], line=dict(color='orange'), name='SMA_50'),
                  row=1, col=1)

    # --- Golden/Death crosses
    golden_idx = df.index[df['golden_cross']==1]
    fig.add_trace(go.Scatter(x=golden_idx, y=df.loc[golden_idx, 'Close'],
                             mode='markers', marker=dict(color='green', size=10, symbol='triangle-up'),
                             name='Golden Cross'), row=1, col=1)
    death_idx = df.index[df['death_cross']==1]
    fig.add_trace(go.Scatter(x=death_idx, y=df.loc[death_idx, 'Close'],
                             mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'),
                             name='Death Cross'), row=1, col=1)

    # --- Volume
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume',
                         marker_color='grey', opacity=0.4),
                  row=2, col=1)

    # --- MACD
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='green')),
                  row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal', line=dict(color='red')),
                  row=3, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_hist'], name='Hist', marker_color='grey', opacity=0.4),
                  row=3, col=1)

    # --- RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI_14'], name='RSI', line=dict(color='purple')),
                  row=4, col=1)
    # Overbought/oversold lines
    fig.add_hline(y=70, line_dash='dash', line_color='red', row=4, col=1)
    fig.add_hline(y=30, line_dash='dash', line_color='green', row=4, col=1)

    # --- Layout
    fig.update_layout(title=f"{symbol} Dashboard",
                      xaxis_rangeslider_visible=False,
                      width=1000, height=900, template='plotly_dark',
                      legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))

    # Show interactive plot
    fig.show()

    # Save as HTML
    fig.write_html(f"charts/{symbol}_dashboard.html")

    # Save as PNG
    fig.write_image(f"charts/{symbol}_dashboard.png")


print("Refreshing dashboard...")

# Run your data fetch script
os.system("python scripts/fetch_data.py")

# Run feature creation script
os.system("python scripts/create_features.py")

# Build dashboard
os.system("python scripts/multi_symbol_dashboard.py")

print("Dashboard updated!")
