# Manual Testing Guide - All 6 Tasks

## Prerequisites
1. Server must be running: `python run_app.py`
2. Server should be accessible at: `http://localhost:5000`

---

## ✅ Task 1: Real-Time Stock Data with Polygon.io

### Test Command:
```bash
curl "http://localhost:5000/api/realtime/quote/AAPL?exchange=US"
```

### Expected Result:
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "price": 178.25,
    "change": 1.75,
    "changePct": 0.99,
    "volume": 45678900,
    "source": "Polygon.io",
    "timestamp": "2025-10-18T12:15:30"
  }
}
```

### ✅ Pass Criteria:
- `success` is `true`
- `price` is a valid number
- `source` is "Polygon.io" or "Yahoo Finance"
- Data is recent (check timestamp)

---

## ✅ Task 2: Stock Search and Selection Interface

### Test Command 1 - Search:
```bash
curl "http://localhost:5000/api/realtime/search?q=APPLE"
```

### Expected Result:
```json
{
  "success": true,
  "query": "APPLE",
  "results": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "exchange": "US",
      "sector": "Technology"
    }
  ],
  "count": 1
}
```

### Test Command 2 - Popular Stocks:
```bash
curl "http://localhost:5000/api/realtime/search"
```

### Expected Result:
```json
{
  "success": true,
  "results": [
    {"symbol": "AAPL", "name": "Apple Inc.", ...},
    {"symbol": "GOOGL", "name": "Alphabet Inc.", ...},
    ...
  ],
  "count": 10
}
```

### ✅ Pass Criteria:
- Search returns matching stocks
- Popular stocks list returns 10+ stocks
- Each stock has symbol, name, exchange, sector

---

## ✅ Task 3: Real-Time ML Prediction Endpoint

### Test Command:
```bash
curl "http://localhost:5000/api/realtime/predict/TSLA?exchange=US"
```

### Expected Result:
```json
{
  "success": true,
  "symbol": "TSLA",
  "quote": {
    "symbol": "TSLA",
    "price": 242.50,
    "change": 3.25,
    "changePct": 1.36
  },
  "prediction": {
    "action": "BUY",
    "confidence": 78,
    "target_price": 255.30,
    "predicted_change": 5.28,
    "risk_level": "Low",
    "timeframe": "7 days"
  }
}
```

### ✅ Pass Criteria:
- `success` is `true`
- `action` is one of: BUY, SELL, HOLD
- `confidence` is between 0-100
- `target_price` is a valid number
- `risk_level` is Low, Medium, or High

---

## ✅ Task 4: Live Data with Auto-Refresh

### Test Method:
Run the same quote command multiple times with delays:

```bash
# Run 1
curl "http://localhost:5000/api/realtime/quote/GOOGL?exchange=US"
# Wait 5 seconds
timeout /t 5
# Run 2
curl "http://localhost:5000/api/realtime/quote/GOOGL?exchange=US"
# Wait 5 seconds
timeout /t 5
# Run 3
curl "http://localhost:5000/api/realtime/quote/GOOGL?exchange=US"
```

### ✅ Pass Criteria:
- All 3 requests return successfully
- Timestamps are different
- Prices may vary slightly (real-time data)
- Response time < 2 seconds

### Browser Test:
```javascript
// Open browser console at http://localhost:5000
// Run this code:

let count = 0;
const interval = setInterval(async () => {
    count++;
    const response = await fetch('/api/realtime/quote/AAPL?exchange=US');
    const data = await response.json();
    console.log(`Update ${count}: $${data.data.price} at ${data.data.timestamp}`);
    
    if (count >= 5) {
        clearInterval(interval);
        console.log('Auto-refresh test complete!');
    }
}, 5000);
```

---

## ✅ Task 5: Popular Stocks List and Watchlist

### Test Command 1 - Get Watchlist:
```bash
curl "http://localhost:5000/api/realtime/watchlist"
```

### Expected Result:
```json
{
  "success": true,
  "watchlist": ["AAPL", "GOOGL", "TSLA", "RELIANCE", "TCS"]
}
```

### Test Command 2 - Add to Watchlist:
```bash
curl -X POST "http://localhost:5000/api/realtime/watchlist" ^
  -H "Content-Type: application/json" ^
  -d "{\"symbol\": \"NVDA\", \"action\": \"add\"}"
```

### Expected Result:
```json
{
  "success": true,
  "watchlist": ["AAPL", "GOOGL", "TSLA", "RELIANCE", "TCS", "NVDA"]
}
```

### Test Command 3 - Remove from Watchlist:
```bash
curl -X POST "http://localhost:5000/api/realtime/watchlist" ^
  -H "Content-Type: application/json" ^
  -d "{\"symbol\": \"NVDA\", \"action\": \"remove\"}"
```

### ✅ Pass Criteria:
- GET returns default watchlist
- POST with "add" adds stock to watchlist
- POST with "remove" removes stock from watchlist
- Watchlist persists during session

---

## ✅ Task 6: Complete System Test (Indian Stocks)

### Test Command 1 - Indian Stock Quote:
```bash
curl "http://localhost:5000/api/realtime/quote/RELIANCE?exchange=NSE"
```

### Expected Result:
```json
{
  "success": true,
  "data": {
    "symbol": "RELIANCE",
    "price": 2456.75,
    "change": 12.50,
    "changePct": 0.51,
    "source": "Yahoo Finance"
  }
}
```

### Test Command 2 - Indian Stock Prediction:
```bash
curl "http://localhost:5000/api/realtime/predict/TCS?exchange=NSE"
```

### Expected Result:
```json
{
  "success": true,
  "symbol": "TCS",
  "prediction": {
    "action": "HOLD",
    "confidence": 72,
    "target_price": 3645.20
  }
}
```

### Test Command 3 - Multiple Exchanges:
```bash
# US Stock
curl "http://localhost:5000/api/realtime/quote/AAPL?exchange=US"

# Indian Stock (NSE)
curl "http://localhost:5000/api/realtime/quote/INFY?exchange=NSE"

# Indian Stock (BSE)
curl "http://localhost:5000/api/realtime/quote/HDFCBANK?exchange=BSE"
```

### ✅ Pass Criteria:
- All exchanges work (US, NSE, BSE)
- Indian stocks return data in INR
- US stocks return data in USD
- Predictions work for both markets

---

## 🎯 Complete System Test Checklist

Run through all these tests:

- [ ] Task 1: Real-time data from Polygon.io/Yahoo Finance
- [ ] Task 2: Stock search returns results
- [ ] Task 2: Popular stocks list works
- [ ] Task 3: ML predictions return BUY/SELL/HOLD
- [ ] Task 3: Confidence scores are valid
- [ ] Task 4: Multiple requests work (auto-refresh)
- [ ] Task 4: Timestamps update correctly
- [ ] Task 5: Get watchlist works
- [ ] Task 5: Add to watchlist works
- [ ] Task 5: Remove from watchlist works
- [ ] Task 6: Indian stocks (NSE) work
- [ ] Task 6: Indian stock predictions work
- [ ] Task 6: Multiple exchanges supported

---

## 🚀 Automated Test

Instead of manual testing, run the automated test script:

```bash
python test_realtime_system.py
```

This will test all 6 tasks automatically and generate a report.

---

## 🆘 Troubleshooting

### Problem: "Connection refused"
**Solution:** Make sure server is running: `python run_app.py`

### Problem: "404 Not Found"
**Solution:** Check the URL is correct: `http://localhost:5000/api/realtime/...`

### Problem: "success: false"
**Solution:** Check server logs for errors. May need to wait for data sources.

### Problem: "Timeout"
**Solution:** 
- Check internet connection
- Polygon.io API may be rate-limited
- Try Yahoo Finance fallback (will happen automatically)

---

## ✅ Success Indicators

All tests pass if you see:
- ✅ Real-time prices updating
- ✅ ML predictions with confidence scores
- ✅ Stock search working
- ✅ Watchlist management working
- ✅ Both US and Indian stocks working
- ✅ Auto-refresh capability confirmed

---

## 📊 Expected Performance

- **Response Time:** < 2 seconds
- **Cache Hit Rate:** ~80% (after first request)
- **Success Rate:** > 95%
- **Data Freshness:** < 30 seconds old

---

**Ready to test? Start the server and run through these tests!** 🚀
