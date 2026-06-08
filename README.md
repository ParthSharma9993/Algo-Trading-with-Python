<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:203a43,100:2c5364&height=200&section=header&text=AlgoTrade-ML&fontSize=60&fontColor=00d4ff&fontAlignY=38&desc=ML-Powered%20Algorithmic%20Trading%20System&descAlignY=58&descSize=18&descColor=a8dadc" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Core-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Pipeline-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Joblib](https://img.shields.io/badge/Joblib-Model%20Serialization-green?style=for-the-badge)](https://joblib.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **A production-grade, modular algorithmic trading system** that integrates a trained ML model for real-time signal generation, live trade execution, and automated position management — built end-to-end in Python.

<br/>

[Overview](#-overview) • [Architecture](#-system-architecture) • [Tech Stack](#-tech-stack) • [Pipeline](#-ml-pipeline) • [Setup](#-installation) • [Usage](#-usage) • [File Structure](#-file-structure)

</div>

---

## 🎯 Overview

AlgoTrade-ML is not a backtesting toy — it's a **live trading system** with a full ML lifecycle baked in. The system fetches real-time market data, runs it through a pre-trained machine learning model to generate buy/sell signals, and executes orders automatically while tracking positions persistently across restarts.

### What makes this different from a typical ML notebook?

| Typical ML Project | AlgoTrade-ML |
|---|---|
| Trains a model, shows accuracy metrics | Trains → serializes → deploys model into a live loop |
| Runs once, outputs a result | Continuous execution loop with configurable intervals |
| No state management | Persistent position tracking via CSV — survives restarts |
| Monolithic script | Modular pipeline: fetch → train → signal → execute |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AlgoTrade-ML Pipeline                    │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Data Layer  │───▶│  ML Engine   │───▶│ Trade Engine │  │
│  │              │    │              │    │              │  │
│  │ fetch_data   │    │ train_model  │    │ live_trader  │  │
│  │    .py       │    │    .py       │    │    .py       │  │
│  │              │    │              │    │              │  │
│  │ • OHLCV data │    │ • Feature    │    │ • Signal     │  │
│  │ • Multi-     │    │   engineering│    │   evaluation │  │
│  │   symbol     │    │ • Model fit  │    │ • Order exec │  │
│  │ • Raw CSV    │    │ • joblib save│    │ • Position   │  │
│  └──────────────┘    └──────────────┘    │   tracking   │  │
│                                          └──────┬───────┘  │
│                                                 │           │
│                             ┌───────────────────▼────────┐ │
│                             │       Persistence Layer     │ │
│                             │  trade_logs/positions.csv   │ │
│                             │  • Open positions restored  │ │
│                             │  • Survives system restart  │ │
│                             └────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

### Core Language
| Tool | Version | Role |
|------|---------|------|
| **Python** | 3.8+ | Primary language |

### Machine Learning
| Library | Role |
|---------|------|
| **Scikit-learn** | Model training — classification/regression for signal generation |
| **Joblib** | Model serialization (`my_model.joblib`) — zero-overhead reload for live inference |
| **NumPy** | Numerical operations, feature arrays |
| **Pandas** | Data ingestion, feature engineering, time-series manipulation |

### Trading & Data
| Library | Role |
|---------|------|
| **yfinance / custom fetch** | Real-time and historical OHLCV market data ingestion |
| **CSV / trade_logs** | Persistent position tracking across restarts |

### Visualization & Analysis
| Library | Role |
|---------|------|
| **Matplotlib / Plotly** | `plot_advanced.py` — signal overlays, P&L curves, trade distribution |

### Dev & Ops
| Tool | Role |
|------|------|
| **Virtual Environment** | Isolated dependency management (`forex_venv`) |
| **requirements.txt** | Reproducible installs |
| **.gitignore** | Clean repo hygiene |

---

## 🧠 ML Pipeline

The ML lifecycle is fully implemented — from raw data to live inference:

```
Step 1: Data Collection
───────────────────────
fetch_data.py
  └── Pulls OHLCV data for configured symbols
  └── Saves to data/ as raw CSV files

Step 2: Feature Engineering + Model Training
─────────────────────────────────────────────
train_model.py
  └── Loads raw market data
  └── Engineers features (returns, rolling stats, indicators)
  └── Trains ML classifier/regressor
  └── Evaluates on held-out data
  └── Serializes → models/my_model.joblib

Step 3: Live Signal Generation + Execution
───────────────────────────────────────────
live_trader.py (continuous loop)
  └── Fetches latest market data
  └── Loads my_model.joblib (zero re-training overhead)
  └── Generates BUY / SELL / HOLD signal
  └── Places order if signal threshold met
  └── Updates trade_logs/positions.csv
  └── Sleeps → SLEEP_SECONDS → repeats
```

### Key Design Decisions

**Why joblib for model persistence?**
Joblib is purpose-built for serializing large NumPy arrays (which underpin Scikit-learn models). It's faster and more memory-efficient than pickle for ML artifacts — enabling sub-millisecond model reload in the live loop.

**Why CSV for position tracking?**
Lightweight, inspectable, and crash-safe. The live trader restores open positions from `trade_logs/positions.csv` on startup — meaning a system restart or network drop doesn't leave orphaned positions untracked.

**Why a modular script structure?**
Each concern (fetch, train, execute, visualize) is a separate module. You can retrain the model independently, swap data sources, or update the signal logic without touching the execution engine.

---

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ParthSharma-2/Algo-Trading-with-Python.git
cd Algo-Trading-with-Python

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Step 1 — Fetch historical market data

```bash
python scripts/fetch_data.py
```

Downloads OHLCV data for all configured symbols into `data/`.

### Step 2 — Train the ML model

```bash
python scripts/train_model.py
```

Trains the model on historical data and saves it to `models/my_model.joblib`. Check console output for evaluation metrics.

### Step 3 — Run the live trader

```bash
python scripts/live_trader.py
```

Starts the live trading loop. The system will:
- Load the serialized model
- Restore any open positions from `trade_logs/positions.csv`
- Begin the fetch → signal → execute → log cycle

### Step 4 — Visualize performance (optional)

```bash
python scripts/plot_advanced.py
```

Generates signal overlay charts, trade logs, and P&L visualizations.

---

## ⚙️ Configuration

All key parameters are defined at the top of `scripts/live_trader.py`:

```python
# ── CONFIGURATION ──────────────────────────────────────────
SYMBOLS        = ["AAPL", "TSLA", "GOOGL"]   # Assets to trade
SLEEP_SECONDS  = 60                           # Loop interval (seconds)
POSITION_SIZE  = 10                           # Units per trade
MODEL_PATH     = "models/my_model.joblib"     # Path to serialized model
LOG_PATH       = "trade_logs/positions.csv"   # Position persistence file
# ────────────────────────────────────────────────────────────
```

---

## 📂 File Structure

```
Algo-Trading-with-Python/
│
├── data/                        # Raw OHLCV market data (CSV per symbol)
│
├── models/
│   └── my_model.joblib          # Serialized trained ML model
│
├── scripts/
│   ├── live_trader.py           # 🔴 Core: live trading loop + order execution
│   ├── train_model.py           # Model training + joblib serialization
│   ├── fetch_data.py            # Market data ingestion
│   └── plot_advanced.py         # Visualization: signals, P&L, trade logs
│
├── stock-ml-genai-starter/      # Experimental GenAI integration starter
│
├── trade_logs/
│   └── positions.csv            # Persistent open position state
│
├── dashboards/                  # Dashboard assets and visualizations
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🔍 What I Learned / Design Highlights

- **Full ML lifecycle in production context** — not just training, but serialization, deployment into a live loop, and inference at runtime
- **State persistence without a database** — CSV-based position tracking is lightweight but robust enough for the use case
- **Modular separation of concerns** — each script is independently runnable and testable, which mirrors real production ML system design
- **Configurable parameters** — all trading variables are surfaced at the top of the execution script, not buried in logic

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

```bash
# Contribution flow
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# → Open a Pull Request
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c5364,50:203a43,100:0f2027&height=100&section=footer" width="100%"/>

**Built by [Parth Sharma](https://www.linkedin.com/in/parth-sharma-work)**
· [GitHub](https://github.com/ParthSharma-2) · [LinkedIn](https://www.linkedin.com/in/parth-sharma-work)

</div>
