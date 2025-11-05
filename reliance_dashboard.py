"""
Real-Time Dashboard for Reliance Stock
Simple Flask app that displays live Reliance stock data
"""

from flask import Flask, render_template_string
import yfinance as yf
from datetime import datetime
import json

app = Flask(__name__)

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Reliance Stock - Real-Time Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }
        
        .header h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .symbol {
            color: #667eea;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .last-update {
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        
        .price-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .current-price {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .price-change {
            font-size: 1.5em;
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
            margin-top: 10px;
        }
        
        .positive {
            background: #10b981;
        }
        
        .negative {
            background: #ef4444;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .stat-value {
            color: #333;
            font-size: 1.5em;
            font-weight: bold;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
            font-size: 1.2em;
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1em;
            cursor: pointer;
            width: 100%;
            transition: background 0.3s;
        }
        
        .refresh-btn:hover {
            background: #764ba2;
        }
        
        .auto-refresh {
            text-align: center;
            color: #10b981;
            font-weight: bold;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Reliance Industries</h1>
            <div class="symbol">RELIANCE.NS</div>
        </div>
        
        <div id="dashboard-content">
            <div class="loading">⏳ Loading real-time data...</div>
        </div>
        
        <button class="refresh-btn" onclick="loadData()">🔄 Refresh Now</button>
        <div class="auto-refresh">⚡ Auto-refreshing every 10 seconds</div>
    </div>
    
    <script>
        function formatNumber(num) {
            if (num >= 1e12) return '₹' + (num / 1e12).toFixed(2) + 'T';
            if (num >= 1e9) return '₹' + (num / 1e9).toFixed(2) + 'B';
            if (num >= 1e6) return '₹' + (num / 1e6).toFixed(2) + 'M';
            if (num >= 1e3) return '₹' + (num / 1e3).toFixed(2) + 'K';
            return '₹' + num.toFixed(2);
        }
        
        function loadData() {
            fetch('/api/reliance')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        document.getElementById('dashboard-content').innerHTML = 
                            '<div class="error">❌ ' + data.error + '</div>';
                        return;
                    }
                    
                    const changeClass = data.change >= 0 ? 'positive' : 'negative';
                    const changeSymbol = data.change >= 0 ? '▲' : '▼';
                    
                    const html = `
                        <div class="last-update">
                            Last Updated: ${data.timestamp}
                        </div>
                        
                        <div class="price-section">
                            <div class="current-price">₹${data.price.toFixed(2)}</div>
                            <div class="price-change ${changeClass}">
                                ${changeSymbol} ₹${Math.abs(data.change).toFixed(2)} 
                                (${data.change_percent.toFixed(2)}%)
                            </div>
                        </div>
                        
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-label">Day High</div>
                                <div class="stat-value">₹${data.day_high.toFixed(2)}</div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Day Low</div>
                                <div class="stat-value">₹${data.day_low.toFixed(2)}</div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Open</div>
                                <div class="stat-value">₹${data.open.toFixed(2)}</div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Previous Close</div>
                                <div class="stat-value">₹${data.prev_close.toFixed(2)}</div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Volume</div>
                                <div class="stat-value">${formatNumber(data.volume)}</div>
                            </div>
                            
                            <div class="stat-card">
                                <div class="stat-label">Market Cap</div>
                                <div class="stat-value">${formatNumber(data.market_cap)}</div>
                            </div>
                        </div>
                    `;
                    
                    document.getElementById('dashboard-content').innerHTML = html;
                })
                .catch(error => {
                    document.getElementById('dashboard-content').innerHTML = 
                        '<div class="error">❌ Failed to load data: ' + error.message + '</div>';
                });
        }
        
        // Load data immediately
        loadData();
        
        // Auto-refresh every 10 seconds
        setInterval(loadData, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Render the dashboard page"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/reliance')
def get_reliance_data():
    """Fetch real-time Reliance stock data"""
    try:
        # Fetch Reliance stock data from Yahoo Finance
        ticker = yf.Ticker("RELIANCE.NS")
        
        # Get current data
        info = ticker.info
        hist = ticker.history(period="1d")
        
        if hist.empty:
            return {
                'error': 'No data available. Market might be closed or symbol invalid.'
            }
        
        # Get the latest data point
        latest = hist.iloc[-1]
        
        # Calculate change
        current_price = latest['Close']
        prev_close = info.get('previousClose', latest['Open'])
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close else 0
        
        # Prepare response
        data = {
            'symbol': 'RELIANCE.NS',
            'price': float(current_price),
            'change': float(change),
            'change_percent': float(change_percent),
            'day_high': float(latest['High']),
            'day_low': float(latest['Low']),
            'open': float(latest['Open']),
            'prev_close': float(prev_close),
            'volume': int(latest['Volume']),
            'market_cap': info.get('marketCap', 0),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return data
        
    except Exception as e:
        return {
            'error': f'Error fetching data: {str(e)}'
        }

if __name__ == '__main__':
    print("=" * 60)
    print("RELIANCE STOCK DASHBOARD - STARTING")
    print("=" * 60)
    print("\nDashboard URL: http://localhost:5001")
    print("Network URL: http://127.0.0.1:5001")
    print("\nAuto-refresh: Every 10 seconds")
    print("Stock: Reliance Industries (RELIANCE.NS)")
    print("\nPress CTRL+C to stop the server\n")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
