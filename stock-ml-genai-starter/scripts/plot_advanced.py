import pandas as pd
import mplfinance as mpf
import plotly.io as pio

# Symbols to plot
symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'SPY', 'EURUSD=X', 'GBPUSD=X']

for symbol in symbols:
    print(f"\n=== Plotting {symbol} ===")
    
    df = pd.read_csv(f"data/{symbol}_features.csv", index_col=0, parse_dates=True)

    # Candlestick chart data must include Volume
    N = 100  # choose window you want to plot
    df_candle = df[['Open', 'High', 'Low', 'Close', 'Volume']].copy().iloc[-N:]
    df = df.iloc[-N:]  # also cut indicators so arrows match


    # Add SMA_20 & SMA_50 as extra plots
    apds = [
        mpf.make_addplot(df['SMA_20'], color='blue'),
        mpf.make_addplot(df['SMA_50'], color='orange')
    ]

    # Find golden/death crosses: get index where they are 1
    golden_idx = df.index[df['golden_cross'] == 1]
    death_idx = df.index[df['death_cross'] == 1]

    # Custom markers: plot as scatter plots over price
    fig, axes = mpf.plot(df_candle, type='candle', style='yahoo',
                         addplot=apds, volume=True, returnfig=True,
                         title=f"{symbol} - Candlestick with SMA & Crosses",
                         figsize=(12,6))
    
    ax = axes[0]  # main price axis

    # Plot golden crosses with green up arrow
    ax.scatter(golden_idx, df.loc[golden_idx, 'Close'],
               marker='^', color='green', s=100, label='Golden Cross')

    # Plot death crosses with red down arrow
    ax.scatter(death_idx, df.loc[death_idx, 'Close'],
               marker='v', color='red', s=100, label='Death Cross')

    ax.legend()

    pio.show()
