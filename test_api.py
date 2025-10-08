#!/usr/bin/env python3
"""
Test script for Healthcare Assistant API
"""

import requests
import json
import time

def test_api():
    """Test the Healthcare Assistant API endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing Healthcare Assistant API...")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✓ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
    
    print()
    
    # Test models info endpoint
    print("2. Testing models info endpoint...")
    try:
        response = requests.get(f"{base_url}/models/info")
        if response.status_code == 200:
            print("   ✓ Models info retrieved")
            data = response.json()
            print(f"   Total models: {data['total_models']}")
            for model_name, info in data['models'].items():
                print(f"   - {model_name}: {info['type']} (loaded: {info['loaded']})")
        else:
            print(f"   ✗ Models info failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Models info error: {e}")
    
    print()
    
    # Test prediction endpoint
    print("3. Testing prediction endpoint...")
    test_data = {
        "age": 45,
        "gender": "Male",
        "bmi": 28.5,
        "systolic_bp": 140,
        "diastolic_bp": 90,
        "heart_rate": 75,
        "glucose": 120,
        "cholesterol": 220,
        "hdl_cholesterol": 45,
        "ldl_cholesterol": 150,
        "triglycerides": 180,
        "smoking": 1,
        "alcohol_consumption": 1,
        "exercise_frequency": 2,
        "diet_quality": 3,
        "family_diabetes": 1,
        "family_heart_disease": 0,
        "family_eye_disease": 0,
        "hypertension": 1,
        "previous_stroke": 0,
        "kidney_disease": 0,
        # UCI-specific features
        "chest_pain_type": "Atypical Angina",
        "exercise_angina": 1,
        "st_depression": 1.5,
        "major_vessels": 2,
        "thalassemia": "Fixed Defect"
    }
    
    try:
        response = requests.post(f"{base_url}/predict/all", json=test_data)
        if response.status_code == 200:
            print("   ✓ Prediction successful")
            data = response.json()
            print("   Predictions:")
            for disease, prediction in data['predictions'].items():
                if 'error' not in prediction:
                    print(f"   - {disease}: {prediction['risk_score']:.3f} ({prediction['risk_level']})")
                else:
                    print(f"   - {disease}: Error - {prediction['error']}")
        else:
            print(f"   ✗ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Prediction error: {e}")
    
    print()
    print("API testing completed!")

if __name__ == "__main__":
    test_api()
