# Real-Time Stock Prediction Setup Guide

## ✅ Step 1: Install Required Packages

```bash
pip install requests pandas joblib numpy
```

If you have TensorFlow models (.h5), also install:
```bash
pip install tensorflow
```

---

## ✅ Step 2: Verify Your API Key

Your Finnhub API key is already configured in the code:
```
API_KEY = "d45ih79r01qsugtah6c0d45ih79r01qsugtah6cg"
```

To verify it works, test it:
```bash
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=d45ih79r01qsugtah6c0d45ih79r01qsugtah6cg"
```

You should get JSON with stock data.

---

## ✅ Step 3: Prepare Your Model

The script looks for models at:
```
models/stock_predictor.pkl       # Default model
models/deep-learning/lstm_model.h5  # LSTM model (optional)
```

### Option A: Use Existing Model
If you have a trained model, place it in one of these locations.

### Option B: Create a Dummy Model (for testing)
```python
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression

# Create a simple model for testing
X = np.array([[100, 99], [101, 100], [102, 101]])  # features
y = np.array([101, 102, 103])  # target

model = LinearRegression()
model.fit(X, y)

# Save it
with open('models/stock_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Test model created at models/stock_predictor.pkl")
```

---

## ✅ Step 4: Configure Symbols (Optional)

Edit `realtime_agent.py` to change which stocks to track:

```python
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]  # Change these
```

Available symbols: Any stock ticker (AAPL, GOOGL, MSFT, TSLA, AMZN, RELIANCE, TCS, etc.)

---

## ✅ Step 5: Run the Real-Time Agent

```bash
python realtime_agent.py
```

You should see output like:

```
[2025-11-05 15:45:00] INFO: ======================================================================
[2025-11-05 15:45:00] INFO: REAL-TIME STOCK PREDICTION AGENT
[2025-11-05 15:45:00] INFO: ======================================================================
[2025-11-05 15:45:00] INFO: ✓ Model 'default' loaded successfully
[2025-11-05 15:45:00] INFO: Tracking symbols: AAPL, GOOGL, MSFT, TSLA, AMZN
[2025-11-05 15:45:00] INFO: Update interval: 30 seconds
[2025-11-05 15:45:00] INFO: ======================================================================
[2025-11-05 15:45:00] INFO: Starting real-time prediction loop...

[2025-11-05 15:45:01] INFO: CYCLE 1 - 15:45:01
[2025-11-05 15:45:01] INFO: ======================================================================
[2025-11-05 15:45:01] INFO:   AAPL:
[2025-11-05 15:45:01] INFO:     Current Price: $227.10
[2025-11-05 15:45:01] INFO:     Predicted Price: $228.50
[2025-11-05 15:45:01] INFO:     Change: +0.62%
[2025-11-05 15:45:01] INFO:     Action: BUY (Confidence: 56.2%)
[2025-11-05 15:45:01] INFO:     Method: trained_model
[2025-11-05 15:45:01] INFO:     Indicators: SMA5=226.80, SMA20=225.50, Momentum=+1.40
[2025-11-05 15:45:01] INFO: ======================================================================
[2025-11-05 15:45:01] INFO: Waiting 30 seconds until next update...
```

---

## 🎯 What It Does

1. **Fetches Real-Time Data** - Gets current stock prices from Finnhub API
2. **Loads Trained Model** - Uses your ML/DL model to make predictions
3. **Makes Predictions** - Predicts next price movement
4. **Calculates Indicators** - SMA, momentum, volatility
5. **Repeats Every 30 Seconds** - Continuous real-time updates

---

## 🔧 Configuration Options

### Change Update Interval
```python
INTERVAL = 30  # Change to 60 for 1 minute, 5 for 5 seconds, etc.
```

### Change History Size
```python
HISTORY_SIZE = 60  # Keep last 60 data points
```

### Add More Symbols
```python
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "RELIANCE", "TCS"]
```

### Use Different Model
```python
MODEL_PATHS = {
    "default": "models/your_model.pkl",
    "lstm": "models/deep-learning/your_lstm.h5",
}
```

---

## 📊 Output Explanation

### Prediction Output
```
Current Price: $227.10          # Current stock price
Predicted Price: $228.50        # AI predicted price
Change: +0.62%                  # Percentage change
Action: BUY                     # Trading signal (BUY/SELL/HOLD)
Confidence: 56.2%               # Model confidence (0-100%)
Method: trained_model           # Prediction method
```

### Technical Indicators
```
SMA5: 226.80                    # 5-period Simple Moving Average
SMA20: 225.50                   # 20-period Simple Moving Average
Momentum: +1.40                 # Price momentum
Volatility: 2.15                # Price volatility
```

---

## 🚨 Troubleshooting

### Issue: "No data received for AAPL"
**Solution**: Check your internet connection and API key

### Issue: "Model not found"
**Solution**: Create a test model or place your model in `models/stock_predictor.pkl`

### Issue: "No module named 'requests'"
**Solution**: Install packages: `pip install requests pandas joblib numpy`

### Issue: "Connection timeout"
**Solution**: Finnhub API might be slow. Increase INTERVAL to 60 seconds

### Issue: "TensorFlow not available"
**Solution**: Install TensorFlow if you have .h5 models: `pip install tensorflow`

---

## 🎓 Next Steps

### Option 1: Connect to Dashboard
Once this works, we can integrate it with your Flask dashboard:
```python
# In ai-copilot/app.py
from realtime_agent import fetch_realtime_quote, make_prediction
```

### Option 2: Create REST API
Wrap this in a Flask API:
```python
@app.route('/api/realtime/<symbol>')
def get_realtime(symbol):
    df = fetch_realtime_quote(symbol)
    prediction = make_prediction(symbol, df, model)
    return jsonify(prediction)
```

### Option 3: Store Predictions
Save predictions to a database:
```python
# Store in CSV or database
predictions_df.to_csv('predictions.csv', mode='a')
```

---

## 📈 Example: Using Predictions

```python
# Get prediction
prediction = make_prediction("AAPL", df, model)

# Check if should buy
if prediction['action'] == 'BUY' and prediction['confidence'] > 70:
    print(f"Strong BUY signal for {prediction['symbol']}")
    # Execute trade
```

---

## 🔗 API Reference

### fetch_realtime_quote(symbol)
Fetches current quote from Finnhub

**Parameters:**
- `symbol` (str): Stock ticker (e.g., 'AAPL')

**Returns:**
- DataFrame with columns: symbol, current, high, low, open, prev_close, volume, timestamp

### make_prediction(symbol, df, model)
Makes price prediction

**Parameters:**
- `symbol` (str): Stock ticker
- `df` (DataFrame): Quote data
- `model`: Trained model

**Returns:**
- Dictionary with prediction results

### calculate_indicators(symbol)
Calculates technical indicators

**Parameters:**
- `symbol` (str): Stock ticker

**Returns:**
- Dictionary with SMA, momentum, volatility

---

## 📝 Log Levels

The script logs with different levels:
- **INFO**: Normal operation
- **WARNING**: Non-critical issues (e.g., model not found)
- **ERROR**: Critical issues (e.g., API error)

---

## ⏹️ Stop the Agent

Press `Ctrl+C` to stop the real-time agent gracefully.

---

## 🎯 Success Criteria

✅ Script runs without errors
✅ Fetches real stock data
✅ Makes predictions every 30 seconds
✅ Shows trading signals (BUY/SELL/HOLD)
✅ Displays confidence scores

---

**Status**: ✅ Ready to Use

For next steps, see the main documentation files:
- QUICKSTART.md
- INTEGRATION_GUIDE.md
- README_INTEGRATION.md
