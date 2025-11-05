# Real-Time Stock Analysis API - Complete Guide

## 🚀 Overview

Your dashboard now has complete real-time stock analysis with:
- ✅ Real-time data from Polygon.io (US stocks) + Yahoo Finance (all stocks)
- ✅ ML predictions with BUY/SELL/HOLD signals
- ✅ Stock search and watchlist
- ✅ Support for US and Indian stocks
- ✅ Auto-refresh capability

## 📡 New API Endpoints

### 1. Get Real-Time Quote
**Endpoint:** `GET /api/realtime/quote/<symbol>`

**Parameters:**
- `exchange` (optional): `US`, `NSE`, or `BSE` (default: `US`)

**Example:**
```bash
# US Stock (uses Polygon.io)
curl "http://localhost:5000/api/realtime/quote/AAPL?exchange=US"

# Indian Stock (uses Yahoo Finance/NSE)
curl "http://localhost:5000/api/realtime/quote/RELIANCE?exchange=NSE"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "price": 178.25,
    "open": 176.50,
    "high": 179.00,
    "low": 175.80,
    "close": 178.25,
    "change": 1.75,
    "changePct": 0.99,
    "volume": 45678900,
    "timestamp": "2025-10-18T12:15:30",
    "source": "Polygon.io"
  },
  "timestamp": "2025-10-18T12:15:30"
}
```

### 2. Get ML Prediction
**Endpoint:** `GET /api/realtime/predict/<symbol>`

**Parameters:**
- `exchange` (optional): `US`, `NSE`, or `BSE` (default: `US`)

**Example:**
```bash
# Get prediction for Apple
curl "http://localhost:5000/api/realtime/predict/AAPL?exchange=US"

# Get prediction for Reliance
curl "http://localhost:5000/api/realtime/predict/RELIANCE?exchange=NSE"
```

**Response:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "quote": {
    "symbol": "AAPL",
    "price": 178.25,
    "change": 1.75,
    "changePct": 0.99,
    "volume": 45678900,
    "source": "Polygon.io"
  },
  "prediction": {
    "symbol": "AAPL",
    "action": "BUY",
    "confidence": 78,
    "current_price": 178.25,
    "target_price": 185.50,
    "predicted_change": 4.07,
    "risk_level": "Low",
    "timeframe": "7 days",
    "models_used": 2,
    "timestamp": "2025-10-18T12:15:30"
  },
  "timestamp": "2025-10-18T12:15:30"
}
```

### 3. Search Stocks
**Endpoint:** `GET /api/realtime/search`

**Parameters:**
- `q` (optional): Search query (symbol or company name)

**Example:**
```bash
# Search for stocks
curl "http://localhost:5000/api/realtime/search?q=APPLE"

# Get popular stocks (no query)
curl "http://localhost:5000/api/realtime/search"
```

**Response:**
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

### 4. Manage Watchlist
**Endpoint:** `GET/POST /api/realtime/watchlist`

**GET - Get Watchlist:**
```bash
curl "http://localhost:5000/api/realtime/watchlist"
```

**Response:**
```json
{
  "success": true,
  "watchlist": ["AAPL", "GOOGL", "TSLA", "RELIANCE", "TCS"]
}
```

**POST - Add/Remove Stock:**
```bash
# Add stock to watchlist
curl -X POST "http://localhost:5000/api/realtime/watchlist" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "MSFT", "action": "add"}'

# Remove stock from watchlist
curl -X POST "http://localhost:5000/api/realtime/watchlist" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "MSFT", "action": "remove"}'
```

## 🎯 Supported Stocks

### US Stocks (Polygon.io):
- **Tech:** AAPL, GOOGL, MSFT, NVDA, AMD, META, NFLX
- **Auto:** TSLA
- **Retail:** AMZN
- **Finance:** JPM
- **And thousands more...**

### Indian Stocks (Yahoo Finance/NSE):
- **IT:** TCS, INFY, WIPRO
- **Banking:** HDFCBANK, ICICIBANK, SBIN
- **Energy:** RELIANCE
- **Telecom:** BHARTIARTL
- **FMCG:** ITC
- **Auto:** TATAMOTORS
- **And all NSE/BSE listed stocks...**

## 🔧 How to Use in Your Dashboard

### JavaScript Example:

```javascript
// Get real-time quote
async function getStockQuote(symbol, exchange = 'US') {
    const response = await fetch(`/api/realtime/quote/${symbol}?exchange=${exchange}`);
    const data = await response.json();
    
    if (data.success) {
        console.log(`${symbol}: $${data.data.price} (${data.data.changePct}%)`);
        return data.data;
    }
}

// Get ML prediction
async function getStockPrediction(symbol, exchange = 'US') {
    const response = await fetch(`/api/realtime/predict/${symbol}?exchange=${exchange}`);
    const data = await response.json();
    
    if (data.success) {
        const pred = data.prediction;
        console.log(`${symbol} - ${pred.action} (${pred.confidence}% confidence)`);
        console.log(`Target: $${pred.target_price} (${pred.predicted_change}%)`);
        return data;
    }
}

// Search stocks
async function searchStocks(query) {
    const response = await fetch(`/api/realtime/search?q=${query}`);
    const data = await response.json();
    return data.results;
}

// Auto-refresh example
function startAutoRefresh(symbol, interval = 5000) {
    setInterval(async () => {
        const data = await getStockPrediction(symbol);
        updateDashboard(data);
    }, interval);
}

// Usage
getStockQuote('AAPL', 'US');
getStockPrediction('RELIANCE', 'NSE');
searchStocks('TESLA');
startAutoRefresh('AAPL', 10000); // Refresh every 10 seconds
```

### Python Example:

```python
import requests

BASE_URL = "http://localhost:5000"

# Get real-time quote
def get_quote(symbol, exchange='US'):
    response = requests.get(f"{BASE_URL}/api/realtime/quote/{symbol}", 
                           params={'exchange': exchange})
    return response.json()

# Get prediction
def get_prediction(symbol, exchange='US'):
    response = requests.get(f"{BASE_URL}/api/realtime/predict/{symbol}",
                           params={'exchange': exchange})
    return response.json()

# Search stocks
def search_stocks(query):
    response = requests.get(f"{BASE_URL}/api/realtime/search",
                           params={'q': query})
    return response.json()

# Usage
apple_data = get_quote('AAPL', 'US')
print(f"Apple: ${apple_data['data']['price']}")

reliance_pred = get_prediction('RELIANCE', 'NSE')
print(f"Reliance: {reliance_pred['prediction']['action']}")
```

## 🎨 Frontend Integration Example

### HTML + JavaScript:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Stock Analysis</title>
</head>
<body>
    <h1>Real-Time Stock Analysis</h1>
    
    <!-- Stock Search -->
    <input type="text" id="stockSearch" placeholder="Search stocks...">
    <button onclick="searchStock()">Search</button>
    
    <!-- Stock Display -->
    <div id="stockInfo"></div>
    <div id="prediction"></div>
    
    <!-- Auto-refresh toggle -->
    <label>
        <input type="checkbox" id="autoRefresh" onchange="toggleAutoRefresh()">
        Auto-refresh (10s)
    </label>
    
    <script>
        let refreshInterval = null;
        let currentSymbol = 'AAPL';
        let currentExchange = 'US';
        
        async function searchStock() {
            const query = document.getElementById('stockSearch').value;
            const results = await fetch(`/api/realtime/search?q=${query}`)
                .then(r => r.json());
            
            if (results.results.length > 0) {
                const stock = results.results[0];
                currentSymbol = stock.symbol;
                currentExchange = stock.exchange;
                await updateStock();
            }
        }
        
        async function updateStock() {
            // Get quote
            const quoteData = await fetch(`/api/realtime/quote/${currentSymbol}?exchange=${currentExchange}`)
                .then(r => r.json());
            
            // Get prediction
            const predData = await fetch(`/api/realtime/predict/${currentSymbol}?exchange=${currentExchange}`)
                .then(r => r.json());
            
            // Display
            if (quoteData.success) {
                const quote = quoteData.data;
                document.getElementById('stockInfo').innerHTML = `
                    <h2>${quote.symbol}</h2>
                    <p>Price: $${quote.price}</p>
                    <p>Change: ${quote.change} (${quote.changePct}%)</p>
                    <p>Volume: ${quote.volume.toLocaleString()}</p>
                    <p>Source: ${quote.source}</p>
                `;
            }
            
            if (predData.success) {
                const pred = predData.prediction;
                const actionColor = pred.action === 'BUY' ? 'green' : 
                                   pred.action === 'SELL' ? 'red' : 'orange';
                
                document.getElementById('prediction').innerHTML = `
                    <h3>ML Prediction</h3>
                    <p style="color: ${actionColor}; font-size: 24px; font-weight: bold;">
                        ${pred.action}
                    </p>
                    <p>Confidence: ${pred.confidence}%</p>
                    <p>Target Price: $${pred.target_price}</p>
                    <p>Expected Change: ${pred.predicted_change.toFixed(2)}%</p>
                    <p>Risk Level: ${pred.risk_level}</p>
                    <p>Timeframe: ${pred.timeframe}</p>
                `;
            }
        }
        
        function toggleAutoRefresh() {
            const enabled = document.getElementById('autoRefresh').checked;
            
            if (enabled) {
                refreshInterval = setInterval(updateStock, 10000);
                updateStock(); // Initial update
            } else {
                if (refreshInterval) {
                    clearInterval(refreshInterval);
                    refreshInterval = null;
                }
            }
        }
        
        // Initial load
        updateStock();
    </script>
</body>
</html>
```

## 🚀 Quick Start

### 1. Start the Server
```bash
cd ai-copilot
python run_app.py
```

### 2. Test the APIs
```bash
# Test US stock
curl "http://localhost:5000/api/realtime/quote/AAPL?exchange=US"

# Test Indian stock
curl "http://localhost:5000/api/realtime/quote/RELIANCE?exchange=NSE"

# Test prediction
curl "http://localhost:5000/api/realtime/predict/TSLA?exchange=US"

# Search stocks
curl "http://localhost:5000/api/realtime/search?q=APPLE"
```

### 3. Open Dashboard
Open browser: `http://localhost:5000`

## 📊 Data Sources

| Exchange | Primary Source | Fallback | API Key Required |
|----------|---------------|----------|------------------|
| US | Polygon.io | Yahoo Finance | ✅ Yes (provided) |
| NSE | Yahoo Finance | NSE API | ❌ No |
| BSE | Yahoo Finance | BSE API | ❌ No |

## 🔑 API Keys

Your Polygon.io API key is already configured:
```
POLYGON_API_KEY=Ed9e0RfqV2wJC_46T4DEg9_Gw_Whwb3U
```

## ⚡ Performance

- **Cache Duration:** 30 seconds (configurable)
- **API Timeout:** 10 seconds
- **Recommended Refresh:** 5-10 seconds for real-time
- **Rate Limits:** Polygon.io free tier = 5 requests/minute

## 🎯 Next Steps

1. **Update your frontend** to use these new endpoints
2. **Add auto-refresh** for live updates
3. **Create watchlist UI** for multiple stocks
4. **Add charts** using the historical data
5. **Implement alerts** based on predictions

## 📝 Notes

- All timestamps are in ISO 8601 format
- Prices are in local currency (USD for US, INR for Indian stocks)
- Predictions are for educational purposes only
- Always verify data before making trading decisions

## 🆘 Troubleshooting

**Problem:** "Unable to fetch data"
- Check internet connection
- Verify symbol is correct
- Try different exchange parameter

**Problem:** "Prediction confidence is low"
- Not enough historical data
- High market volatility
- Model needs more training data

**Problem:** "API rate limit exceeded"
- Reduce refresh frequency
- Implement caching on frontend
- Upgrade Polygon.io plan

---

**Your dashboard now has complete real-time stock analysis! 🎉**

Start the server and test the APIs to see live data in action.
