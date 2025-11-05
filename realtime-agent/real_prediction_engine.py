"""
Real-time Stock Prediction Engine
Integrates trained ML/DL models for live stock price predictions
"""

import numpy as np
import pandas as pd
import pickle
import os
import sys
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealPredictionEngine:
    """
    Real-time prediction engine that uses trained ML/DL models
    to predict stock prices based on live market data
    """
    
    def __init__(self, model_path=None, lookback_period=60):
        """
        Initialize the prediction engine
        
        Args:
            model_path: Path to trained model (pickle or h5)
            lookback_period: Number of days to use for prediction context
        """
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.lookback_period = lookback_period
        self.model_path = model_path
        self.last_data = None
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load a trained model from disk"""
        try:
            if model_path.endswith('.pkl'):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"Loaded pickle model from {model_path}")
            elif model_path.endswith('.h5'):
                try:
                    from tensorflow.keras.models import load_model
                    self.model = load_model(model_path)
                    logger.info(f"Loaded Keras model from {model_path}")
                except ImportError:
                    logger.warning("TensorFlow not available, cannot load .h5 models")
            else:
                logger.warning(f"Unknown model format: {model_path}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
    
    def fetch_stock_data(self, symbol, period='1y', interval='1d'):
        """
        Fetch real stock data from Yahoo Finance
        
        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
            period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max')
            interval: Data interval ('1m', '5m', '15m', '30m', '60m', '1d', '1wk', '1mo')
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            logger.info(f"Fetching data for {symbol}...")
            data = yf.download(symbol, period=period, interval=interval, progress=False)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            # Reset index to make Date a column
            if isinstance(data.index, pd.DatetimeIndex):
                data = data.reset_index()
            
            logger.info(f"Fetched {len(data)} records for {symbol}")
            return data
        
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def prepare_features(self, data, feature_columns=['Close']):
        """
        Prepare features for prediction
        
        Args:
            data: DataFrame with stock data
            feature_columns: Columns to use as features
        
        Returns:
            Scaled features and scaler object
        """
        try:
            if data is None or len(data) == 0:
                logger.warning("No data to prepare")
                return None, None
            
            # Extract features
            features = data[feature_columns].values.reshape(-1, len(feature_columns))
            
            # Scale features
            scaled_features = self.scaler.fit_transform(features)
            
            self.last_data = {
                'features': scaled_features,
                'original': features,
                'columns': feature_columns,
                'timestamp': datetime.now()
            }
            
            return scaled_features, self.scaler
        
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return None, None
    
    def create_sequences(self, data, seq_length=60):
        """
        Create sequences for LSTM/sequence models
        
        Args:
            data: Scaled feature data
            seq_length: Length of each sequence
        
        Returns:
            List of sequences
        """
        sequences = []
        for i in range(len(data) - seq_length):
            seq = data[i:i + seq_length]
            sequences.append(seq)
        
        return np.array(sequences) if sequences else None
    
    def predict_price(self, symbol, days_ahead=1):
        """
        Predict future stock price
        
        Args:
            symbol: Stock ticker symbol
            days_ahead: Number of days to predict ahead
        
        Returns:
            Dictionary with prediction results
        """
        try:
            # Fetch recent data
            data = self.fetch_stock_data(symbol, period='1y', interval='1d')
            if data is None:
                return {
                    'symbol': symbol,
                    'error': 'Could not fetch data',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get current price
            current_price = data['Close'].iloc[-1]
            
            # Prepare features
            scaled_features, scaler = self.prepare_features(data, feature_columns=['Close'])
            if scaled_features is None:
                return {
                    'symbol': symbol,
                    'error': 'Could not prepare features',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Create sequences
            sequences = self.create_sequences(scaled_features, seq_length=self.lookback_period)
            if sequences is None or len(sequences) == 0:
                return {
                    'symbol': symbol,
                    'current_price': float(current_price),
                    'error': 'Insufficient data for prediction',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Make prediction using the last sequence
            last_sequence = sequences[-1:] if len(sequences) > 0 else None
            
            if last_sequence is not None and self.model is not None:
                try:
                    prediction = self.model.predict(last_sequence)
                    
                    # Handle different prediction output formats
                    if isinstance(prediction, np.ndarray):
                        if prediction.ndim > 1:
                            predicted_scaled = prediction[0, 0] if prediction.shape[1] > 0 else prediction[0]
                        else:
                            predicted_scaled = prediction[0]
                    else:
                        predicted_scaled = float(prediction)
                    
                    # Inverse transform to get actual price
                    predicted_price = scaler.inverse_transform(
                        np.array([[predicted_scaled]])
                    )[0, 0]
                    
                    price_change = predicted_price - current_price
                    price_change_pct = (price_change / current_price) * 100
                    
                    return {
                        'symbol': symbol,
                        'current_price': float(current_price),
                        'predicted_price': float(predicted_price),
                        'price_change': float(price_change),
                        'price_change_pct': float(price_change_pct),
                        'action': 'BUY' if price_change_pct > 1 else 'SELL' if price_change_pct < -1 else 'HOLD',
                        'confidence': min(abs(price_change_pct) * 10 + 50, 95),
                        'days_ahead': days_ahead,
                        'timestamp': datetime.now().isoformat(),
                        'data_points_used': len(sequences[-1])
                    }
                
                except Exception as e:
                    logger.error(f"Error in model prediction: {e}")
                    # Fallback to simple trend analysis
                    return self._fallback_prediction(symbol, data, current_price)
            
            else:
                # No model loaded, use fallback prediction
                return self._fallback_prediction(symbol, data, current_price)
        
        except Exception as e:
            logger.error(f"Error predicting price for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _fallback_prediction(self, symbol, data, current_price):
        """
        Fallback prediction using simple trend analysis
        """
        try:
            # Calculate simple moving average trend
            sma_20 = data['Close'].tail(20).mean()
            sma_50 = data['Close'].tail(50).mean() if len(data) >= 50 else sma_20
            
            trend = 'up' if sma_20 > sma_50 else 'down'
            trend_strength = abs(sma_20 - sma_50) / sma_50 * 100
            
            # Simple prediction based on trend
            predicted_price = current_price * (1 + (trend_strength / 100) if trend == 'up' else 1 - (trend_strength / 100))
            price_change_pct = ((predicted_price - current_price) / current_price) * 100
            
            return {
                'symbol': symbol,
                'current_price': float(current_price),
                'predicted_price': float(predicted_price),
                'price_change': float(predicted_price - current_price),
                'price_change_pct': float(price_change_pct),
                'action': 'BUY' if price_change_pct > 0.5 else 'SELL' if price_change_pct < -0.5 else 'HOLD',
                'confidence': min(trend_strength + 50, 85),
                'method': 'trend_analysis',
                'trend': trend,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error in fallback prediction: {e}")
            return {
                'symbol': symbol,
                'current_price': float(current_price),
                'error': 'Prediction failed',
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_multiple(self, symbols, days_ahead=1):
        """
        Predict prices for multiple symbols
        
        Args:
            symbols: List of stock ticker symbols
            days_ahead: Number of days to predict ahead
        
        Returns:
            List of prediction results
        """
        predictions = []
        for symbol in symbols:
            pred = self.predict_price(symbol, days_ahead)
            predictions.append(pred)
        
        return predictions
    
    def get_technical_indicators(self, symbol):
        """
        Calculate technical indicators for a stock
        
        Args:
            symbol: Stock ticker symbol
        
        Returns:
            Dictionary with technical indicators
        """
        try:
            data = self.fetch_stock_data(symbol, period='1y', interval='1d')
            if data is None:
                return None
            
            close = data['Close']
            
            # Calculate indicators
            sma_20 = close.tail(20).mean()
            sma_50 = close.tail(50).mean() if len(close) >= 50 else sma_20
            sma_200 = close.tail(200).mean() if len(close) >= 200 else sma_20
            
            # RSI calculation
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # MACD calculation
            exp1 = close.ewm(span=12, adjust=False).mean()
            exp2 = close.ewm(span=26, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            
            current_price = close.iloc[-1]
            
            return {
                'symbol': symbol,
                'current_price': float(current_price),
                'sma_20': float(sma_20),
                'sma_50': float(sma_50),
                'sma_200': float(sma_200),
                'rsi': float(rsi.iloc[-1]) if not rsi.empty else None,
                'macd': float(macd.iloc[-1]) if not macd.empty else None,
                'macd_signal': float(signal.iloc[-1]) if not signal.empty else None,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return None


# Example usage
if __name__ == '__main__':
    # Initialize engine
    engine = RealPredictionEngine(lookback_period=60)
    
    # Test with a stock
    result = engine.predict_price('AAPL')
    print("Prediction Result:")
    print(result)
    
    # Get technical indicators
    indicators = engine.get_technical_indicators('AAPL')
    print("\nTechnical Indicators:")
    print(indicators)
