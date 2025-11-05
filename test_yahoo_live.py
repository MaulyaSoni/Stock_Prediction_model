"""
Test Yahoo Finance real-time data directly
"""
import yfinance as yf
from datetime import datetime

def test_stock(symbol):
    print(f"\n{'='*60}")
    print(f"Testing: {symbol}")
    print(f"{'='*60}")
    
    try:
        ticker = yf.Ticker(symbol)
        
        # Get current info
        info = ticker.info
        print(f"\n📊 Current Data:")
        print(f"   Symbol: {info.get('symbol', 'N/A')}")
        print(f"   Name: {info.get('longName', 'N/A')}")
        print(f"   Current Price: ${info.get('currentPrice', info.get('regularMarketPrice', 0)):.2f}")
        print(f"   Previous Close: ${info.get('previousClose', 0):.2f}")
        print(f"   Open: ${info.get('open', info.get('regularMarketOpen', 0)):.2f}")
        print(f"   Day High: ${info.get('dayHigh', info.get('regularMarketDayHigh', 0)):.2f}")
        print(f"   Day Low: ${info.get('dayLow', info.get('regularMarketDayLow', 0)):.2f}")
        print(f"   Volume: {info.get('volume', info.get('regularMarketVolume', 0)):,}")
        print(f"   Market Cap: ${info.get('marketCap', 0):,}")
        
        # Get intraday data
        hist = ticker.history(period='1d', interval='1m')
        
        if not hist.empty:
            latest = hist.iloc[-1]
            first = hist.iloc[0]
            
            current_price = latest['Close']
            open_price = first['Open']
            change = current_price - open_price
            change_pct = (change / open_price) * 100 if open_price > 0 else 0
            
            print(f"\n📈 Intraday Data (Last Minute):")
            print(f"   Latest Price: ${current_price:.2f}")
            print(f"   Change: ${change:+.2f} ({change_pct:+.2f}%)")
            print(f"   High: ${hist['High'].max():.2f}")
            print(f"   Low: ${hist['Low'].min():.2f}")
            print(f"   Volume: {int(hist['Volume'].sum()):,}")
            print(f"   Last Update: {hist.index[-1]}")
            print(f"   Data Points: {len(hist)} minutes")
            
            return True
        else:
            print("❌ No intraday data available (market may be closed)")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test popular stocks
print("\n" + "="*60)
print("REAL-TIME DATA TEST - Yahoo Finance")
print("="*60)
print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

stocks = [
    ('AAPL', 'Apple'),
    ('TSLA', 'Tesla'),
    ('GOOGL', 'Google'),
    ('MSFT', 'Microsoft'),
    ('RELIANCE.NS', 'Reliance Industries (India)')
]

print("\nTesting 5 stocks...\n")

results = []
for symbol, name in stocks:
    success = test_stock(symbol)
    results.append((symbol, name, success))
    
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
for symbol, name, success in results:
    status = "✅ SUCCESS" if success else "❌ FAILED"
    print(f"{status} - {symbol} ({name})")

print("\n" + "="*60)
