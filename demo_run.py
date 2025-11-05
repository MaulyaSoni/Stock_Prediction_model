"""
Demo Run - Real-Time Stock Prediction Agent
Runs 3 cycles to demonstrate the system working
"""

import requests
import pandas as pd
import joblib
import time
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')

API_KEY = 'd45ih79r01qsugtah6c0d45ih79r01qsugtah6cg'
SYMBOL = 'AAPL'
MODEL_PATH = 'models/stock_predictor.pkl'
FETCH_INTERVAL = 5
FEATURES = ['current', 'prev_close']

def fetch_live_data(symbol):
    try:
        url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
        response = requests.get(url, timeout=10)
        data = response.json()
        
        return {
            'symbol': symbol,
            'current': data.get('c', 0),
            'high': data.get('h', 0),
            'low': data.get('l', 0),
            'open': data.get('o', 0),
            'prev_close': data.get('pc', 0),
            'volume': data.get('v', 0),
            'timestamp': datetime.now()
        }
    except Exception as e:
        print(f'[ERROR] Failed to fetch data: {e}')
        return None

def prepare_input(data):
    df = pd.DataFrame([data])
    X = df[FEATURES].values
    return X

def load_model(model_path):
    try:
        model = joblib.load(model_path)
        print(f'[INFO] Loaded model from: {model_path}')
        return model
    except Exception as e:
        print(f'[ERROR] Failed to load model: {e}')
        return None

print('=' * 70)
print('REAL-TIME STOCK PREDICTION AGENT - DEMO RUN')
print('=' * 70)
print(f'API Key: {API_KEY[:10]}...')
print(f'Symbol: {SYMBOL}')
print(f'Model: {MODEL_PATH}')
print(f'Features: {FEATURES}')
print('=' * 70)

model = load_model(MODEL_PATH)
if model is None:
    print('[ERROR] Could not load model. Exiting.')
    exit(1)

print(f'[INFO] Tracking symbol: {SYMBOL}')
print(f'[INFO] Update interval: {FETCH_INTERVAL} seconds')
print('=' * 70)
print()

# Run for 3 cycles
for cycle in range(1, 4):
    live_data = fetch_live_data(SYMBOL)
    
    if live_data is None:
        print(f'[CYCLE {cycle}] Failed to fetch data.')
        continue
    
    X = prepare_input(live_data)
    
    try:
        prediction = model.predict(X)[0]
    except Exception as e:
        print(f'[ERROR] Prediction failed: {e}')
        continue
    
    price_change = prediction - live_data['current']
    price_change_pct = (price_change / live_data['current']) * 100 if live_data['current'] != 0 else 0
    
    if price_change_pct > 1:
        action = 'BUY'
    elif price_change_pct < -1:
        action = 'SELL'
    else:
        action = 'HOLD'
    
    timestamp_str = live_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    print(f'[CYCLE {cycle}] [{timestamp_str}]')
    print(f'  {SYMBOL} | Current: ${live_data["current"]:.2f} | Predicted: ${prediction:.2f} | Change: {price_change_pct:+.2f}% | Action: {action}')
    print()
    
    if cycle < 3:
        time.sleep(FETCH_INTERVAL)

print('=' * 70)
print('[INFO] Demo run completed successfully!')
print('=' * 70)
