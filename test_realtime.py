"""
Real-Time Stock Analysis Test Script
Run this to see live stock data and predictions
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def get_realtime_quote(symbol, exchange="US"):
    """Get real-time stock quote"""
    try:
        response = requests.get(f"{BASE_URL}/api/realtime/quote/{symbol}", 
                               params={"exchange": exchange})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_prediction(symbol, exchange="US"):
    """Get ML prediction for stock"""
    try:
        response = requests.get(f"{BASE_URL}/api/realtime/predict/{symbol}",
                               params={"exchange": exchange})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def display_quote(data):
    """Display stock quote in formatted way"""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return
    
    quote = data.get("data", {})
    print(f"\n📊 {quote.get('symbol', 'N/A')} - Real-Time Quote")
    print(f"   Price:        ${quote.get('price', 0):.2f}")
    print(f"   Change:       ${quote.get('change', 0):.2f} ({quote.get('changePct', 0):.2f}%)")
    print(f"   Volume:       {quote.get('volume', 0):,}")
    print(f"   Day Range:    ${quote.get('low', 0):.2f} - ${quote.get('high', 0):.2f}")
    print(f"   Market Cap:   {quote.get('marketCap', 'N/A')}")
    print(f"   Source:       {quote.get('source', 'N/A')}")
    print(f"   Timestamp:    {quote.get('timestamp', 'N/A')}")

def display_prediction(data):
    """Display ML prediction in formatted way"""
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return
    
    pred = data.get("data", {})
    signal = pred.get('signal', 'HOLD')
    confidence = pred.get('confidence', 0)
    
    # Signal emoji
    signal_emoji = {
        'BUY': '🟢',
        'SELL': '🔴',
        'HOLD': '🟡'
    }
    
    print(f"\n🤖 ML Prediction for {pred.get('symbol', 'N/A')}")
    print(f"   Signal:       {signal_emoji.get(signal, '⚪')} {signal}")
    print(f"   Confidence:   {confidence:.1f}%")
    print(f"   Current:      ${pred.get('current_price', 0):.2f}")
    print(f"   Predicted 24h: ${pred.get('predicted_price_24h', 0):.2f}")
    print(f"   Predicted 7d:  ${pred.get('predicted_price_7d', 0):.2f}")
    print(f"   Predicted 30d: ${pred.get('predicted_price_30d', 0):.2f}")
    
    indicators = pred.get('technical_indicators', {})
    if indicators:
        print(f"\n   Technical Indicators:")
        print(f"   RSI:          {indicators.get('rsi', 'N/A')}")
        print(f"   MACD:         {indicators.get('macd', 'N/A')}")
        print(f"   Momentum:     {indicators.get('momentum', 'N/A')}")
    
    recommendation = pred.get('recommendation', '')
    if recommendation:
        print(f"\n   💡 {recommendation}")

def analyze_stock(symbol, exchange="US"):
    """Analyze a stock with real-time data and prediction"""
    print_header(f"Analyzing {symbol} ({exchange})")
    
    # Get quote
    print("\n⏳ Fetching real-time quote...")
    quote_data = get_realtime_quote(symbol, exchange)
    display_quote(quote_data)
    
    # Get prediction
    print("\n⏳ Generating ML prediction...")
    pred_data = get_prediction(symbol, exchange)
    display_prediction(pred_data)

def monitor_stocks(symbols, interval=10):
    """Monitor multiple stocks in real-time"""
    print_header("Real-Time Stock Monitoring")
    print(f"\n📡 Monitoring {len(symbols)} stocks (updates every {interval}s)")
    print("Press CTRL+C to stop\n")
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n⏰ Update at {timestamp}")
            print("-" * 80)
            
            for symbol_info in symbols:
                symbol = symbol_info['symbol']
                exchange = symbol_info.get('exchange', 'US')
                
                quote_data = get_realtime_quote(symbol, exchange)
                if "error" not in quote_data:
                    quote = quote_data.get("data", {})
                    price = quote.get('price', 0)
                    change = quote.get('change', 0)
                    change_pct = quote.get('changePct', 0)
                    
                    # Color based on change
                    indicator = "🟢" if change >= 0 else "🔴"
                    
                    print(f"{indicator} {symbol:8s} ${price:8.2f}  {change:+7.2f} ({change_pct:+6.2f}%)")
            
            print("-" * 80)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✋ Monitoring stopped by user")

def main():
    """Main function"""
    print_header("Real-Time Stock Analysis System")
    print("\n🚀 System Status: CONNECTED")
    print(f"📡 API Endpoint: {BASE_URL}")
    print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Menu
    print("\n" + "="*80)
    print("Choose an option:")
    print("="*80)
    print("1. Analyze a single stock (detailed)")
    print("2. Monitor multiple stocks (live updates)")
    print("3. Quick test with popular stocks")
    print("4. Exit")
    print("="*80)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        symbol = input("\nEnter stock symbol (e.g., AAPL, TSLA, RELIANCE.NS): ").strip().upper()
        exchange = "NSE" if ".NS" in symbol else "US"
        analyze_stock(symbol, exchange)
        
    elif choice == "2":
        print("\n📋 Default watchlist: AAPL, GOOGL, MSFT, TSLA, AMZN")
        custom = input("Use default? (y/n): ").strip().lower()
        
        if custom == 'n':
            symbols_input = input("Enter symbols separated by comma (e.g., AAPL,TSLA,MSFT): ")
            symbols = [{'symbol': s.strip().upper(), 'exchange': 'US'} 
                      for s in symbols_input.split(',')]
        else:
            symbols = [
                {'symbol': 'AAPL', 'exchange': 'US'},
                {'symbol': 'GOOGL', 'exchange': 'US'},
                {'symbol': 'MSFT', 'exchange': 'US'},
                {'symbol': 'TSLA', 'exchange': 'US'},
                {'symbol': 'AMZN', 'exchange': 'US'}
            ]
        
        interval = int(input("Update interval in seconds (default 10): ") or "10")
        monitor_stocks(symbols, interval)
        
    elif choice == "3":
        # Quick test with popular stocks
        test_stocks = [
            ('AAPL', 'US'),
            ('TSLA', 'US'),
            ('GOOGL', 'US')
        ]
        
        for symbol, exchange in test_stocks:
            analyze_stock(symbol, exchange)
            print("\n" + "="*80 + "\n")
            time.sleep(2)
    
    elif choice == "4":
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Program interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
