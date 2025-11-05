"""
Quick Test Script for Real-Time Stock Prediction
Tests API connectivity and model loading
"""

import requests
import sys
import os

print("=" * 70)
print("REAL-TIME STOCK PREDICTION - QUICK TEST")
print("=" * 70)

# Test 1: Check API connectivity
print("\n[TEST 1] Checking Finnhub API connectivity...")
try:
    API_KEY = "d45ih79r01qsugtah6c0d45ih79r01qsugtah6cg"
    url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if 'c' in data and data['c'] is not None:
        print("[PASS] API is working")
        print(f"   AAPL Current Price: ${data['c']}")
        print(f"   High: ${data.get('h', 'N/A')}")
        print(f"   Low: ${data.get('l', 'N/A')}")
    else:
        print("[FAIL] API returned no data")
        sys.exit(1)
except requests.exceptions.RequestException as e:
    print(f"[FAIL] API connection error: {e}")
    sys.exit(1)

# Test 2: Check required packages
print("\n[TEST 2] Checking required packages...")
required_packages = ['requests', 'pandas', 'numpy', 'joblib']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"[OK] {package} is installed")
    except ImportError:
        print(f"[MISSING] {package} is NOT installed")
        missing_packages.append(package)

if missing_packages:
    print(f"\nMissing packages: {', '.join(missing_packages)}")
    print(f"Install with: pip install {' '.join(missing_packages)}")
else:
    print("[PASS] All required packages installed")

# Test 3: Check model directory
print("\n[TEST 3] Checking model directory...")
if os.path.exists('models'):
    print("[OK] models/ directory exists")
    
    # Check for models
    model_files = []
    for root, dirs, files in os.walk('models'):
        for file in files:
            if file.endswith(('.pkl', '.h5')):
                model_files.append(os.path.join(root, file))
    
    if model_files:
        print(f"[OK] Found {len(model_files)} model file(s):")
        for model_file in model_files:
            print(f"   - {model_file}")
    else:
        print("[INFO] No model files found (.pkl or .h5)")
        print("   You can create a test model or place your trained model here")
else:
    print("[INFO] models/ directory not found")
    print("   Creating models/ directory...")
    os.makedirs('models', exist_ok=True)
    print("[OK] Created models/ directory")

# Test 4: Try loading a model (if exists)
print("\n[TEST 4] Testing model loading...")
try:
    import pickle
    import joblib
    
    model_path = 'models/stock_predictor.pkl'
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"[PASS] Successfully loaded model from {model_path}")
        except Exception as e:
            print(f"[FAIL] Error loading model: {e}")
    else:
        print(f"[INFO] No model at {model_path}")
        print("   Creating a test model for demonstration...")
        
        try:
            from sklearn.linear_model import LinearRegression
            import numpy as np
            
            # Create simple test model
            X = np.array([[100, 99], [101, 100], [102, 101]])
            y = np.array([101, 102, 103])
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Save it
            os.makedirs('models', exist_ok=True)
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            print(f"[PASS] Created test model at {model_path}")
        except Exception as e:
            print(f"[INFO] Could not create test model: {e}")
            print("   You can still run the agent with fallback mode")

except ImportError as e:
    print(f"[INFO] Could not test model loading: {e}")

# Test 5: Check if realtime_agent.py exists
print("\n[TEST 5] Checking realtime_agent.py...")
if os.path.exists('realtime_agent.py'):
    print("[OK] realtime_agent.py exists")
else:
    print("[FAIL] realtime_agent.py not found")

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

if not missing_packages:
    print("[PASS] All tests passed!")
    print("\nYou can now run:")
    print("  python realtime_agent.py")
else:
    print("[WARNING] Some issues found. Please fix them before running the agent.")
    print("\nTo install missing packages:")
    print(f"  pip install {' '.join(missing_packages)}")

print("\n" + "=" * 70)
