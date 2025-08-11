# Automated Trading System with Python for Stock

## 📖 Description

This repository contains a robust algorithmic trading system built with Python, designed for real-time trade execution in the Stock market. The system automates the process of data fetching, signal generation using a pre-trained model, and order placement. It's built to be modular and easy to manage, with a clear separation of concerns for each part of the trading pipeline.

## ✨ Features

* **Live Trading Execution:** The `live_trader.py` script acts as the core of the system, running a continuous loop to manage trading activities.
* **Machine Learning Integration:** Uses a pre-trained model, saved with `joblib`, to generate trading signals.
* **Persistent Position Tracking:** Automatically restores open positions from a log file (`trade_logs/positions.csv`) to ensure continuity even after restarting the script.
* **Modular Scripts:** The `scripts` directory contains separate modules for key functionalities, including data fetching (`fetch_data.py`), model training (`train_model.py`), and data visualization (`plot_advanced.py`).
* **Configuration:** Key trading parameters like `SYMBOLS`, `SLEEP_SECONDS`, and `POSITION_SIZE` are easily configurable at the top of the `live_trader.py` script.
* **Dependency Management:** A `requirements.txt` file and a dedicated virtual environment (`Stock_venv`) are included for easy setup.

## ⚙️ Prerequisites

To run this project, you need:

* **Python** (3.8 or higher)
* **pip** (Python package installer)

## 🔧 Installation

1.  **Clone the repository:**

    ```
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Activate the virtual environment:**
    The project uses a virtual environment named `Stock_venv`.

    ```
    # On Windows
    Stock_venv\Scripts\activate
    # On macOS/Linux
    source Stock_venv/bin/activate
    ```

3.  **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

## 🚀 Getting Started

1.  **Prepare your data and model:**

    * Use `train_model.py` to train your machine learning model and save it as `my_model.joblib` in the `models/` directory.
    * Ensure your historical data is available in the `data/` directory.

2.  **Configure the live trader:**
    Open `scripts/live_trader.py` and adjust the configuration settings at the top, such as the `SYMBOLS` list to define the assets you want to trade and `POSITION_SIZE` for your risk management.

3.  **Run the live trading script:**
    With your virtual environment active, execute the main trading script.

    ```
    python scripts/live_trader.py
    ```

    The script will begin its trading loop and will automatically log all trading activities to the `trade_logs/` directory.

## 📂 File Structure

The project has a clear and logical file structure:
