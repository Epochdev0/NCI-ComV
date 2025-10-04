#!/usr/bin/env python3
"""Test script for the Exo-Vision Explorer compatible FastAPI server."""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_simple_prediction():
    """Test the simplified prediction endpoint for Exo-Vision Explorer."""
    print("Testing Exo-Vision Explorer compatible prediction...")
    
    # Example exoplanet features matching the frontend
    features = {
        "koi_period": 15.5,
        "koi_depth": 0.005,
        "koi_duration": 3.2,
        "koi_steff": 5800
    }
    
    try:
        response = requests.post(f"{BASE_URL}/predict", json=features)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction: {result['prediction']} (0=false positive, 1=exoplanet)")
            print(f"✅ Probability: {result['probability']:.3f}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_extended_prediction():
    """Test the extended prediction endpoint."""
    print("\nTesting extended prediction...")
    
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
        response = requests.post(f"{BASE_URL}/predict/extended", json=features)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction: {result['prediction']} (0=false positive, 1=exoplanet)")
            print(f"✅ Probability: {result['probability']:.3f}")
            print(f"✅ Kepler ID: {result.get('kepid', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    """Test the health endpoint."""
    print("\nTesting health endpoint...")
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

def main():
    """Run all tests."""
    print("🚀 Testing Exo-Vision Explorer Compatible FastAPI Server")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Simple Prediction (Exo-Vision)", test_simple_prediction),
        ("Extended Prediction", test_extended_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(0.5)  # Small delay between tests
    
    print(f"\n{'='*60}")
    print("📊 Test Results:")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your API is ready for Exo-Vision Explorer!")
        print("\n📋 Next steps:")
        print("1. Start your FastAPI server: python src/api.py")
        print("2. Update the Exo-Vision Explorer frontend to point to your API")
        print("3. Replace the Supabase function call with direct API calls")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()
