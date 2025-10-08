#!/usr/bin/env python3
"""
Basic usage example for Healthcare Assistant API
"""

import requests
import json

# API base URL
API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/health")
    print("Health Status:", response.json())

def test_prediction():
    """Test disease prediction"""
    # Sample patient data
    patient_data = {
        "age": 45,
        "gender": "Male",
        "bmi": 25.5,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "heart_rate": 70,
        "glucose": 100,
        "cholesterol": 200,
        "hdl_cholesterol": 50,
        "ldl_cholesterol": 120,
        "triglycerides": 150,
        "smoking": 0,
        "alcohol_consumption": 1,
        "exercise_frequency": 2,
        "diet_quality": 3,
        "family_diabetes": 0,
        "family_heart_disease": 0,
        "family_eye_disease": 0,
        "hypertension": 0,
        "previous_stroke": 0,
        "kidney_disease": 0
    }
    
    # Get predictions
    response = requests.post(
        f"{API_URL}/predict/all",
        json=patient_data
    )
    
    if response.status_code == 200:
        predictions = response.json()
        print("Disease Risk Predictions:")
        for disease, risk in predictions.items():
            print(f"  {disease}: {risk['risk_level']} ({risk['risk_score']:.2f})")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    print("Testing Healthcare Assistant API...")
    test_health()
    test_prediction()
