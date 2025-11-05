"""
Real-Time Stock Prediction Agent
--------------------------------
Continuously fetches live stock prices from Finnhub API and uses a trained ML/DL model
to predict the next price movement or value.

Author: AI Trading System
Project: Stock_Prediction_Models
"""

import requests
import pandas as pd
import joblib
import time
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ================= CONFIG ==================
API_KEY = "d45ih79r01qsugtah6c0d45ih79r01qsugtah6cg"  # ✅ Finnhub API Key

# Available tickers to choose from
AVAILABLE_TICKERS = {
    "1": {"symbol": "AAPL", "name": "Apple Inc.", "type": "Stock"},
    "2": {"symbol": "BTC", "name": "Bitcoin", "type": "Crypto"},
    "3": {"symbol": "ETH", "name": "Ethereum", "type": "Crypto"},
    "4": {"symbol": "SOL", "name": "Solana", "type": "Crypto"},
    "5": {"symbol": "XRP", "name": "Ripple", "type": "Crypto"},
}

# Default symbol (change this or select at runtime)
SYMBOL = "AAPL"                   # Options: AAPL, BTC, ETH, SOL, XRP

MODEL_PATH = "models/stock_predictor.pkl"  # 🔹 Path to your trained model
FETCH_INTERVAL = 30               # 🔹 Fetch every 30 seconds (adjust as needed)
FEATURES = ["current", "prev_close"]  # 🔹 Must match your model's input features
# ===========================================


# === Function: Fetch Real-Time Stock Data ===
def fetch_live_data(symbol):
    """
    Fetch real-time stock data from Finnhub API
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
    
    Returns:
        Dictionary with current quote data
    """
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        return {
            "symbol": symbol,
            "current": data.get("c", 0),      # Current price
            "high": data.get("h", 0),         # High
            "low": data.get("l", 0),          # Low
            "open": data.get("o", 0),         # Open
            "prev_close": data.get("pc", 0),  # Previous close
            "volume": data.get("v", 0),       # Volume
            "timestamp": datetime.now()
        }
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
        return None


# === Function: Prepare Input for Model ===
def prepare_input(data):
    """
    Convert live data into model-ready format
    
    Args:
        data: Dictionary with stock data
    
    Returns:
        Feature array ready for model prediction
    """
    df = pd.DataFrame([data])
    X = df[FEATURES].values
    return X


# === Function: Load Model ===
def load_model(model_path):
    """
    Load trained model from disk
    
    Args:
        model_path: Path to model file (.pkl or .h5)
    
    Returns:
        Loaded model or None if error
    """
    try:
        if model_path.endswith('.pkl'):
            model = joblib.load(model_path)
            print(f"[INFO] [OK] Loaded model from: {model_path}")
            return model
        elif model_path.endswith('.h5'):
            from tensorflow.keras.models import load_model as keras_load
            model = keras_load(model_path)
            print(f"[INFO] [OK] Loaded Keras model from: {model_path}")
            return model
        else:
            print(f"[ERROR] Unknown model format: {model_path}")
            return None
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return None


# === Function: Display Ticker Selection Menu ===
def display_ticker_menu():
    """
    Display available tickers and let user choose
    
    Returns:
        Selected symbol (str)
    """
    print("\n" + "=" * 70)
    print("AVAILABLE TICKERS")
    print("=" * 70)
    
    for key, ticker_info in AVAILABLE_TICKERS.items():
        print(f"{key}. {ticker_info['symbol']:6} - {ticker_info['name']:20} ({ticker_info['type']})")
    
    print("=" * 70)
    
    while True:
        choice = input("\nSelect ticker (1-5) or press Enter for default (AAPL): ").strip()
        
        if choice == "":
            return "AAPL"
        
        if choice in AVAILABLE_TICKERS:
            selected = AVAILABLE_TICKERS[choice]['symbol']
            print(f"\n[INFO] Selected: {selected}")
            return selected
        else:
            print("[ERROR] Invalid choice. Please select 1-5 or press Enter.")


# === Main Real-Time Prediction Loop ===
def run_realtime_prediction(symbol=None):
    """
    Continuously fetch data, predict, and print results
    
    This is the main loop that:
    1. Fetches live stock data every FETCH_INTERVAL seconds
    2. Prepares features for the model
    3. Makes predictions
    4. Displays results in real-time
    """
    print(f"\n[START] Starting Real-Time Prediction for {SYMBOL}")
    print("=" * 70)

    # Load trained model
    model = load_model(MODEL_PATH)
    if model is None:
        print("[ERROR] Could not load model. Exiting.")
        return
    
    print(f"[INFO] Tracking symbol: {SYMBOL}")
    print(f"[INFO] Update interval: {FETCH_INTERVAL} seconds")
    print("=" * 70)
    print()

    cycle = 0
    
    try:
        while True:
            cycle += 1
            
            # Fetch live data
            live_data = fetch_live_data(SYMBOL)
            
            if live_data is None:
                print(f"[CYCLE {cycle}] Failed to fetch data. Retrying in {FETCH_INTERVAL}s...")
                time.sleep(FETCH_INTERVAL)
                continue
            
            # Prepare input for model
            X = prepare_input(live_data)
            
            # Make prediction
            try:
                prediction = model.predict(X)[0]
            except Exception as e:
                print(f"[ERROR] Prediction failed: {e}")
                time.sleep(FETCH_INTERVAL)
                continue
            
            # Calculate price change
            price_change = prediction - live_data['current']
            price_change_pct = (price_change / live_data['current']) * 100 if live_data['current'] != 0 else 0
            
            # Determine action
            if price_change_pct > 1:
                action = "[BUY]"
            elif price_change_pct < -1:
                action = "[SELL]"
            else:
                action = "[HOLD]"
            
            # Print results
            print(f"[CYCLE {cycle}] [{live_data['timestamp']:%Y-%m-%d %H:%M:%S}]")
            print(f"  {SYMBOL} | Current: ${live_data['current']:.2f} | "
                  f"Predicted: ${prediction:.2f} | "
                  f"Change: {price_change_pct:+.2f}% | "
                  f"Action: {action}")
            print()

            # Wait for next cycle
            time.sleep(FETCH_INTERVAL)

    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("[INFO] Real-time prediction stopped by user")
        print("=" * 70)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        raise


# === Run App ===
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("REAL-TIME STOCK PREDICTION AGENT")
    print("=" * 70)
    print(f"API Key: {API_KEY[:10]}...")
    print(f"Symbol: {SYMBOL}")
    print(f"Model: {MODEL_PATH}")
    print(f"Features: {FEATURES}")
    print("=" * 70)
    
    run_realtime_prediction()
