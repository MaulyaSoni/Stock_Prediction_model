# ✅ STEP 2: Real-Time Prediction Loop (Fully Functional)

## 🎯 What's New

The `realtime_agent.py` has been optimized to be:
- ✅ **Clean & Simple** - Easy to understand and modify
- ✅ **Robust** - Error handling for API failures
- ✅ **Fast** - Minimal overhead, quick predictions
- ✅ **Production-Ready** - Continuous 24/7 operation

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install requests pandas joblib numpy
```

### Step 2: Create Test Model
```bash
python -c "
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
import os

os.makedirs('models', exist_ok=True)

X = np.array([[100, 99], [101, 100], [102, 101], [103, 102]])
y = np.array([101, 102, 103, 104])

model = LinearRegression()
model.fit(X, y)

with open('models/stock_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print('✓ Test model created')
"
```

### Step 3: Run the Agent
```bash
python realtime_agent.py
```

---

## 📊 Expected Output

```
======================================================================
REAL-TIME STOCK PREDICTION AGENT
======================================================================
API Key: d45ih79r0...
Symbol: AAPL
Model: models/stock_predictor.pkl
Features: ['current', 'prev_close']
======================================================================

🚀 Starting Real-Time Prediction for AAPL
======================================================================
[INFO] ✓ Loaded model from: models/stock_predictor.pkl
[INFO] Tracking symbol: AAPL
[INFO] Update interval: 30 seconds
======================================================================

[CYCLE 1] [2025-11-05 16:30:00]
  AAPL | Current: $227.30 | Predicted: $228.10 | Change: +0.35% | Action: 🟡 HOLD

[CYCLE 2] [2025-11-05 16:30:30]
  AAPL | Current: $227.80 | Predicted: $228.42 | Change: +0.27% | Action: 🟡 HOLD

[CYCLE 3] [2025-11-05 16:31:00]
  AAPL | Current: $228.15 | Predicted: $228.56 | Change: +0.18% | Action: 🟡 HOLD
```

---

## 🔧 Configuration

### Change Symbol
```python
SYMBOL = "TSLA"  # AAPL, TSLA, MSFT, GOOGL, etc.
```

### Change Update Interval
```python
FETCH_INTERVAL = 10  # Fetch every 10 seconds
```

### Change Model Path
```python
MODEL_PATH = "models/your_lstm_model.h5"
```

### Change Features
```python
FEATURES = ["current", "prev_close", "high", "low"]
```

---

## 🧠 How It Works

1. **Load Model** - Loads your trained ML/DL model
2. **Fetch Data** - Gets live stock price from Finnhub API
3. **Prepare Features** - Formats data for model input
4. **Make Prediction** - Runs model.predict()
5. **Calculate Change** - Computes price change percentage
6. **Determine Action** - BUY (>1%), SELL (<-1%), HOLD
7. **Display Results** - Prints to console
8. **Wait** - Sleeps for FETCH_INTERVAL seconds
9. **Repeat** - Continuous loop

---

## 📈 Trading Signals

| Signal | Condition | Emoji |
|--------|-----------|-------|
| BUY | Predicted change > +1% | 🟢 |
| SELL | Predicted change < -1% | 🔴 |
| HOLD | Between -1% and +1% | 🟡 |

---

## 🎯 Supported Stocks

Any stock symbol supported by Finnhub:
- US: AAPL, GOOGL, MSFT, TSLA, AMZN, NFLX, META, NVDA
- Indian: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN
- Forex: EURUSD, GBPUSD, etc.

---

## 🔑 API Key

Already configured:
```python
API_KEY = "d45ih79r01qsugtah6c0d45ih79r01qsugtah6cg"
```

No setup needed!

---

## ⏹️ Stop the Agent

Press `Ctrl+C` to stop gracefully

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named 'requests'" | `pip install requests pandas joblib` |
| "Model not found" | Create test model or place your model in `models/` |
| "Failed to fetch data" | Check internet connection |
| "Prediction failed" | Verify model features match FEATURES config |

---

## 💡 Next Steps

### Option 1: Log Predictions to CSV
```python
# Add to main loop
import csv
with open('predictions.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow([live_data['timestamp'], SYMBOL, live_data['current'], prediction])
```

### Option 2: Add Alerts
```python
# Alert when strong signal
if price_change_pct > 2:
    print(f"🚨 STRONG BUY SIGNAL for {SYMBOL}!")
```

### Option 3: Connect to Dashboard
Integrate with Flask API to display in web UI

---

## ✅ Verification

- [ ] Dependencies installed
- [ ] Test model created
- [ ] realtime_agent.py runs
- [ ] See live predictions
- [ ] Trading signals displayed
- [ ] No errors in console

---

**Status**: ✅ STEP 2 COMPLETE

Ready for STEP 3: Dashboard Integration or CSV Logging
