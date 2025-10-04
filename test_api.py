#!/usr/bin/env python3
"""Test script for the Exoplanet Classification FastAPI server."""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Start it with: python src/api.py")
        return False

def test_model_info():
    """Test the model info endpoint."""
    print("\nTesting model info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_single_prediction():
    """Test single prediction endpoint."""
    print("\nTesting single prediction...")
    
    # Example exoplanet features (from the NASA dataset)
    features = {
        "kepid": 10797460,
        "koi_period": 9.48803557,
        "koi_depth": 615.8,
        "koi_duration": 2.9575,
        "koi_impact": 0.146,
        "koi_model_snr": 35.8,
        "koi_steff": 5455,
        "koi_slogg": 4.467,
        "koi_srad": 0.927,
        "koi_kepmag": 15.347,
        "ra": 291.93423,
        "dec": 48.141651
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=features)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction: {result['prediction']} (0=false positive, 1=planet)")
            print(f"✅ Probability: {result['probability']:.3f}")
            print(f"✅ Kepler ID: {result['kepid']}")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint."""
    print("\nTesting batch prediction...")
    
    # Multiple exoplanet candidates
    features_list = [
        {
            "kepid": 10797460,
            "koi_period": 9.48803557,
            "koi_depth": 615.8,
            "koi_duration": 2.9575,
            "koi_impact": 0.146,
            "koi_model_snr": 35.8,
            "koi_steff": 5455,
            "koi_slogg": 4.467,
            "koi_srad": 0.927,
            "koi_kepmag": 15.347,
            "ra": 291.93423,
            "dec": 48.141651
        },
        {
            "kepid": 12345678,
            "koi_period": 12.34567890,
            "koi_depth": 800.5,
            "koi_duration": 3.2,
            "koi_impact": 0.3,
            "koi_model_snr": 25.8,
            "koi_steff": 5200,
            "koi_slogg": 4.2,
            "koi_srad": 1.1,
            "koi_kepmag": 14.5,
            "ra": 300.0,
            "dec": 50.0
        }
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/predict/batch", json=features_list)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Processed {result['total_samples']} candidates")
            for i, pred in enumerate(result['predictions']):
                print(f"  Candidate {i+1}: {pred['prediction']} (prob: {pred['probability']:.3f})")
        else:
            print(f"❌ Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Exoplanet Classification FastAPI Server")
    print("=" * 50)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(0.5)  # Small delay between tests
    
    print(f"\n{'='*50}")
    print("📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()
