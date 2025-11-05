"""
Enhanced Real-time Stock Prediction API
Serves real predictions from trained ML/DL models via REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from real_prediction_engine import RealPredictionEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize prediction engine
engine = RealPredictionEngine(lookback_period=60)

# Popular Indian stocks
POPULAR_STOCKS = {
    'RELIANCE': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'INFY': 'INFOSY.NS',
    'HDFCBANK': 'HDFCBANK.NS',
    'ICICIBANK': 'ICICIBANK.NS',
    'SBIN': 'SBIN.NS',
    'BHARTIARTL': 'BHARTIARTL.NS',
    'ITC': 'ITC.NS',
    'AAPL': 'AAPL',
    'GOOGL': 'GOOGL',
    'MSFT': 'MSFT',
    'TSLA': 'TSLA',
}

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Real-time Stock Prediction Engine',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/predict/<symbol>', methods=['GET'])
def predict_single(symbol):
    """
    Predict price for a single stock
    
    Query parameters:
    - days_ahead: Number of days to predict ahead (default: 1)
    
    Example: /api/predict/AAPL?days_ahead=1
    """
    try:
        days_ahead = request.args.get('days_ahead', 1, type=int)
        
        # Map symbol if it's a shorthand
        actual_symbol = POPULAR_STOCKS.get(symbol, symbol)
        
        logger.info(f"Predicting for {actual_symbol}")
        prediction = engine.predict_price(actual_symbol, days_ahead)
        
        return jsonify(prediction)
    
    except Exception as e:
        logger.error(f"Error in predict_single: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict prices for multiple stocks
    
    Request body:
    {
        "symbols": ["AAPL", "GOOGL", "MSFT"],
        "days_ahead": 1
    }
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        days_ahead = data.get('days_ahead', 1)
        
        if not symbols:
            return jsonify({'error': 'No symbols provided'}), 400
        
        # Map symbols if they're shorthands
        actual_symbols = [POPULAR_STOCKS.get(s, s) for s in symbols]
        
        logger.info(f"Predicting for {len(actual_symbols)} symbols")
        predictions = engine.predict_multiple(actual_symbols, days_ahead)
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in predict_batch: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/technicals/<symbol>', methods=['GET'])
def get_technicals(symbol):
    """
    Get technical indicators for a stock
    
    Example: /api/technicals/AAPL
    """
    try:
        # Map symbol if it's a shorthand
        actual_symbol = POPULAR_STOCKS.get(symbol, symbol)
        
        logger.info(f"Getting technicals for {actual_symbol}")
        indicators = engine.get_technical_indicators(actual_symbol)
        
        if indicators is None:
            return jsonify({'error': 'Could not fetch data'}), 404
        
        return jsonify(indicators)
    
    except Exception as e:
        logger.error(f"Error in get_technicals: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/top-predictions', methods=['GET'])
def top_predictions():
    """
    Get predictions for top popular stocks
    
    Query parameters:
    - count: Number of stocks to predict (default: 8)
    """
    try:
        count = request.args.get('count', 8, type=int)
        
        stocks = list(POPULAR_STOCKS.items())[:count]
        predictions = []
        
        logger.info(f"Getting top {count} predictions")
        
        for short_name, full_symbol in stocks:
            pred = engine.predict_price(full_symbol)
            predictions.append(pred)
        
        # Sort by confidence
        predictions.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in top_predictions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stock-data/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """
    Get current stock data with prediction and technicals
    
    Example: /api/stock-data/AAPL
    """
    try:
        # Map symbol if it's a shorthand
        actual_symbol = POPULAR_STOCKS.get(symbol, symbol)
        
        logger.info(f"Getting full data for {actual_symbol}")
        
        # Get prediction
        prediction = engine.predict_price(actual_symbol)
        
        # Get technical indicators
        technicals = engine.get_technical_indicators(actual_symbol)
        
        return jsonify({
            'symbol': actual_symbol,
            'prediction': prediction,
            'technicals': technicals,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_stock_data: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/supported-stocks', methods=['GET'])
def supported_stocks():
    """Get list of supported stocks"""
    return jsonify({
        'stocks': POPULAR_STOCKS,
        'count': len(POPULAR_STOCKS),
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Get information about the prediction model"""
    return jsonify({
        'model_loaded': engine.model is not None,
        'model_path': engine.model_path,
        'lookback_period': engine.lookback_period,
        'data_source': 'Yahoo Finance',
        'supported_symbols': len(POPULAR_STOCKS),
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info("Starting Enhanced Real-time Stock Prediction API")
    logger.info(f"Model loaded: {engine.model is not None}")
    logger.info(f"Supported stocks: {len(POPULAR_STOCKS)}")
    
    app.run(host='0.0.0.0', port=8005, debug=False)
