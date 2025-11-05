# Real-time Stock Data Integration Guide

## Overview

This project now supports **real-time stock data** from multiple sources including:
- **NSE (National Stock Exchange of India)**
- **BSE (Bombay Stock Exchange)**
- **Yahoo Finance** (Primary source - Free & Reliable)
- **Kotak Neo API** (Already configured)
- **Alpha Vantage** (Optional)
- **Twelve Data** (Optional)

The system uses a **multi-source fallback mechanism** to ensure data availability even if one source fails.

---

## Quick Start (No API Keys Required!)

The easiest way to get started is using **Yahoo Finance**, which requires **no API keys**:

### 1. Install Dependencies

```bash
cd ai-copilot
pip install -r requirements.txt
```

### 2. Create Environment File

```bash
# Copy the example file
copy .env.example .env

# Edit .env and set:
USE_YAHOO_FINANCE=true
USE_DUMMY_DATA=false
```

### 3. Run the Application

```bash
python dashboard_app.py
```

That's it! The application will automatically fetch real-time data from Yahoo Finance for Indian stocks (NSE/BSE).

---

## Advanced Setup (With API Keys)

For production use or higher rate limits, you can configure additional data sources:

### NSE API Configuration

**Note:** NSE doesn't provide official public APIs. The system uses web scraping with proper headers.

```env
NSE_API_KEY=not_required
NSE_BASE_URL=https://www.nseindia.com/api
```

### BSE API Configuration

**Getting BSE API Access:**
1. Visit: https://www.bseindia.com/
2. Contact BSE for API access (requires registration)
3. Add credentials to `.env`:

```env
BSE_API_KEY=your_bse_api_key
BSE_API_SECRET=your_bse_api_secret
BSE_BASE_URL=https://api.bseindia.com
```

### Kotak Neo API (Already Configured)

```env
KOTAK_API_TOKEN=b2f4fe81-4fdb-4b61-b6e1-8820a4b69a73
KOTAK_BASE_URL=https://gw-napi.kotaksecurities.com
```

### Alpha Vantage (Optional - Free Tier Available)

**Getting Alpha Vantage API Key:**
1. Visit: https://www.alphavantage.co/support/#api-key
2. Sign up for free API key (500 requests/day)
3. Add to `.env`:

```env
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

### Twelve Data (Optional - Free Tier Available)

**Getting Twelve Data API Key:**
1. Visit: https://twelvedata.com/
2. Sign up for free API key (800 requests/day)
3. Add to `.env`:

```env
TWELVE_DATA_API_KEY=your_twelve_data_key
```

---

## Configuration Options

### Environment Variables

Edit `.env` file to customize behavior:

```env
# Data Sources
USE_YAHOO_FINANCE=true          # Use Yahoo Finance (recommended)
USE_DUMMY_DATA=false            # Use dummy data for testing

# API Rate Limiting
API_RATE_LIMIT_PER_MINUTE=60   # Max API calls per minute
API_TIMEOUT_SECONDS=10          # Request timeout
CACHE_DURATION_SECONDS=30       # Cache data for 30 seconds

# Data Refresh
REAL_TIME_UPDATE_INTERVAL=5     # Update every 5 seconds

# Market Hours (IST)
MARKET_OPEN_TIME=09:15
MARKET_CLOSE_TIME=15:30

# Development
DEBUG_MODE=false
```

---

## Supported Stock Symbols

The system supports all NSE and BSE listed stocks. Common symbols include:

### Top NSE Stocks
- **RELIANCE** - Reliance Industries
- **TCS** - Tata Consultancy Services
- **INFY** - Infosys
- **HDFCBANK** - HDFC Bank
- **ICICIBANK** - ICICI Bank
- **SBIN** - State Bank of India
- **BHARTIARTL** - Bharti Airtel
- **ITC** - ITC Limited
- **LT** - Larsen & Toubro
- **AXISBANK** - Axis Bank
- **KOTAKBANK** - Kotak Mahindra Bank
- **HCLTECH** - HCL Technologies
- **MARUTI** - Maruti Suzuki
- **TATAMOTORS** - Tata Motors
- **TATASTEEL** - Tata Steel
- **WIPRO** - Wipro
- **SUNPHARMA** - Sun Pharma
- **ASIANPAINT** - Asian Paints
- **BAJFINANCE** - Bajaj Finance

### Market Indices
- **^NSEI** - NIFTY 50
- **^BSESN** - SENSEX
- **^NSEBANK** - BANK NIFTY

---

## API Endpoints

### Get Real-time Stock Quote

```bash
GET /api/stock_realtime/<symbol>
```

**Example:**
```bash
curl http://localhost:5000/api/stock_realtime/RELIANCE
```

**Response:**
```json
{
  "symbol": "RELIANCE",
  "price": 2500.50,
  "open": 2485.00,
  "high": 2520.00,
  "low": 2480.00,
  "change": 15.50,
  "changePct": 0.62,
  "volume": 5234567,
  "timestamp": "2024-10-16T16:30:00",
  "source": "Yahoo Finance",
  "market_cap": 16950000000000,
  "pe_ratio": 28.5
}
```

### Get Market Indices

```bash
GET /api/indian_indices
```

**Response:**
```json
{
  "indices": [
    {
      "name": "NIFTY 50",
      "symbol": "^NSEI",
      "value": 19500.50,
      "change": 150.25,
      "changePct": 0.77
    },
    {
      "name": "SENSEX",
      "symbol": "^BSESN",
      "value": 65432.10,
      "change": 200.50,
      "changePct": 0.31
    }
  ],
  "timestamp": "2024-10-16T16:30:00"
}
```

### Get Top Gainers/Losers

```bash
GET /api/top_movers
```

### Get Historical Data

Use the `realtime_fetcher` module in Python:

```python
from realtime_data_fetcher import get_realtime_fetcher

fetcher = get_realtime_fetcher()

# Get 1 month of daily data
df = fetcher.get_historical_data('RELIANCE', period='1mo', interval='1d')

# Get 5 days of 15-minute data
df = fetcher.get_historical_data('TCS', period='5d', interval='15m')
```

---

## Data Source Priority

The system tries data sources in this order:

1. **Yahoo Finance** (if enabled) - Most reliable, free, no API key
2. **NSE API** (if configured) - Direct from exchange
3. **BSE API** (if configured) - Direct from exchange
4. **Kotak Neo API** (fallback) - Already configured
5. **Dummy Data** (last resort) - For testing only

---

## Caching Strategy

To optimize performance and respect API rate limits:

- **Cache Duration:** 30 seconds (configurable)
- **Cache Keys:** Based on symbol and exchange
- **Auto-refresh:** During market hours only
- **Smart Updates:** Prices update only when market is open

---

## Market Hours

The system respects Indian market hours:

- **Pre-market:** 09:00 - 09:15 IST
- **Regular Trading:** 09:15 - 15:30 IST
- **Post-market:** 15:30 - 16:00 IST

Prices are **frozen** outside market hours to reflect last traded price.

---

## Testing the Integration

### Test Script

Run the test script to verify all data sources:

```bash
python realtime_data_fetcher.py
```

**Expected Output:**
```
Testing Real-time Data Fetcher...

1. Testing Stock Quote (RELIANCE):
   Symbol: RELIANCE
   Price: ₹2500.50
   Change: +15.50 (+0.62%)
   Source: Yahoo Finance

2. Testing Market Indices:
   NIFTY 50: 19500.50 (+0.77%)
   SENSEX: 65432.10 (+0.31%)

3. Testing Historical Data (TCS, 5 days):
   Retrieved 5 data points
   Latest Close: ₹3600.25

4. Testing Top Gainers/Losers:
   Top Gainers:
     NESTLEIND: +3.08%
     BAJAJFINSV: +2.60%
     ASIANPAINT: +1.97%

Test Complete!
```

### Web Interface Test

1. Start the application:
```bash
python dashboard_app.py
```

2. Open browser: http://localhost:5000

3. Check the dashboard for real-time data

---

## Troubleshooting

### Issue: "No data available"

**Solution:**
1. Check internet connection
2. Verify `.env` file exists and `USE_YAHOO_FINANCE=true`
3. Try different stock symbol
4. Check if market is open (data updates only during market hours)

### Issue: "Rate limit exceeded"

**Solution:**
1. Increase `CACHE_DURATION_SECONDS` in `.env`
2. Reduce `API_RATE_LIMIT_PER_MINUTE`
3. Use multiple API sources for load balancing

### Issue: "Yahoo Finance not working"

**Solution:**
1. Update yfinance: `pip install --upgrade yfinance`
2. Check symbol format (should be `SYMBOL.NS` for NSE, `SYMBOL.BO` for BSE)
3. Try alternative data source by setting `USE_YAHOO_FINANCE=false`

### Issue: "Import errors"

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

---

## Performance Optimization

### For High-Frequency Updates

```env
# Reduce cache duration for more frequent updates
CACHE_DURATION_SECONDS=5

# Increase rate limit (if API allows)
API_RATE_LIMIT_PER_MINUTE=120
```

### For Production Deployment

```env
# Increase cache to reduce API calls
CACHE_DURATION_SECONDS=60

# Enable multiple data sources for redundancy
USE_YAHOO_FINANCE=true
ALPHA_VANTAGE_API_KEY=your_key
TWELVE_DATA_API_KEY=your_key
```

---

## Best Practices

1. **Always use caching** to respect API rate limits
2. **Enable multiple data sources** for redundancy
3. **Monitor API usage** to avoid hitting limits
4. **Update during market hours only** to save API calls
5. **Use appropriate intervals** (1m for intraday, 1d for long-term)
6. **Handle errors gracefully** with fallback mechanisms

---

## API Rate Limits

| Source | Free Tier | Paid Tier | Notes |
|--------|-----------|-----------|-------|
| Yahoo Finance | Unlimited* | N/A | *Fair use policy applies |
| NSE | N/A | N/A | Web scraping (use responsibly) |
| BSE | Contact BSE | Contact BSE | Requires registration |
| Alpha Vantage | 500/day | 5-1200/min | Free tier sufficient for testing |
| Twelve Data | 800/day | 8-800/min | Good free tier |
| Kotak Neo | Contact Kotak | Contact Kotak | Already configured |

---

## Support & Resources

### Documentation
- Yahoo Finance: https://pypi.org/project/yfinance/
- NSE India: https://www.nseindia.com/
- BSE India: https://www.bseindia.com/
- Alpha Vantage: https://www.alphavantage.co/documentation/
- Twelve Data: https://twelvedata.com/docs

### Community
- GitHub Issues: Report bugs and request features
- Stack Overflow: Tag with `yfinance`, `nse-india`, `stock-market`

---

## License

This integration follows the same license as the main project (Apache License 2.0).

---

## Changelog

### Version 1.0.0 (Current)
- ✅ Multi-source data integration (NSE, BSE, Yahoo Finance)
- ✅ Automatic fallback mechanism
- ✅ Smart caching with configurable duration
- ✅ Market hours awareness
- ✅ Support for 50+ popular Indian stocks
- ✅ Real-time indices tracking
- ✅ Historical data fetching
- ✅ Top gainers/losers tracking
- ✅ Environment-based configuration

---

## Next Steps

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Configure environment:** Copy `.env.example` to `.env`
3. **Run application:** `python dashboard_app.py`
4. **Access dashboard:** http://localhost:5000
5. **Start trading!** 🚀

For questions or issues, please open a GitHub issue or contact the development team.
