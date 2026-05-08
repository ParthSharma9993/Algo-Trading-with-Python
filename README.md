# Automated Trading System with Python for Stocks Trading

## 📖 Description

This repository contains a robust algorithmic trading system built with Python, designed for real-time trade execution in the stock market. The system automates the process of data fetching, signal generation using a pre-trained model, and order placement. It's built to be modular and easy to manage, with a clear separation of concerns for each part of the trading pipeline.

## ✨ Features

* **Live Trading Execution:** The `live_trader.py` script acts as the core of the system, running a continuous loop to manage trading activities.
* **Machine Learning Integration:** Uses a pre-trained model, saved with `joblib`, to generate trading signals.
* **Persistent Position Tracking:** Automatically restores open positions from a log file (`trade_logs/positions.csv`) to ensure continuity even after restarting the script.
* **Modular Scripts:** The `scripts` directory contains separate modules for key functionalities, including data fetching (`fetch_data.py`), model training (`train_model.py`), and data visualization (`plot_advanced.py`).
* **Configuration:** Key trading parameters like `SYMBOLS`, `SLEEP_SECONDS`, and `POSITION_SIZE` are easily configurable at the top of the `live_trader.py` script.
* **Dependency Management:** A `requirements.txt` file and a dedicated virtual environment (`forex_venv`) are included for easy setup.

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
    The project uses a virtual environment named `forex_venv`.

    ```
    # On Windows
    forex_venv\Scripts\activate
    # On macOS/Linux
    source forex_venv/bin/activate
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

To see the content of the README.md file in a code block format, you can use the following markdown. This is the exact content that would be displayed on GitHub.



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
    The project uses a virtual environment named `forex_venv`.

    ```
    # On Windows
    forex_venv\Scripts\activate
    # On macOS/Linux
    source forex_venv/bin/activate
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

.
├── data/                       # Market data for various symbols.
├── dashboards/                 # Files for visualization and dashboards.
├── forex-ml-genai-starter/     # Main project directory.
├── forex_venv/                 # Virtual environment.
├── models/                     # Directory to store the trained machine learning model.
│   └── my_model.joblib
├── scripts/                    # All executable scripts.
│   ├── live_trader.py          # Core live trading script.
│   ├── train_model.py          # Script for training the model.
│   ├── fetch_data.py           # Script to fetch market data.
│   └── ...
├── trade_logs/                 # Automatically generated logs of trades.
│   └── positions.csv
├── README.md                   # This file.
└── requirements.txt            # Project dependencies.

## 🤝 Contributing

This project is a great starting point for algorithmic trading. Feel free to fork the repository, add your own strategies, and contribute back to the community!

1.  Fork the Project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
