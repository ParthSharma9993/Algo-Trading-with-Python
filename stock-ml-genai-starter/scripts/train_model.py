# Build & train ML model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'SPY']
all_data = []

for symbol in symbols:
    df = pd.read_csv(f"data/{symbol}_features.csv", index_col=0, parse_dates=True)

    # Create target: price increase over next 5 mins
    df['future_close'] = df['Close'].shift(-5)
    df['target'] = (df['future_close'] > df['Close']).astype(int)

    # Drop last rows without future_close
    df.dropna(inplace=True)

    # Add symbol column (if want to train single model over all symbols)
    df['symbol'] = symbol

    all_data.append(df)

# Combine all
df_all = pd.concat(all_data)

# --- Features
features = ['Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_hist']
# plus: you can add 'golden_cross', 'death_cross', etc.

X = df_all[features]
y = df_all['target']

# --- Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# --- Train
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# --- Save model
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/price_direction_rf.pkl')
print("✅ Model saved as models/price_direction_rf.pkl")
