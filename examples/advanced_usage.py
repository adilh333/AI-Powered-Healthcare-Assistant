#!/usr/bin/env python3
"""
Advanced usage example for Healthcare Assistant
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class HealthcareClient:
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
    
    def get_health_status(self):
        """Get API health status"""
        response = requests.get(f"{self.api_url}/health")
        return response.json()
    
    def get_model_info(self):
        """Get model information"""
        response = requests.get(f"{self.api_url}/models/info")
        return response.json()
    
    def predict_disease(self, patient_data, disease_type="all"):
        """Predict disease risk"""
        endpoint = f"/predict/{disease_type}" if disease_type != "all" else "/predict/all"
        response = requests.post(f"{self.api_url}{endpoint}", json=patient_data)
        return response.json()
    
    def batch_predict(self, patients_df):
        """Predict for multiple patients"""
        results = []
        for _, patient in patients_df.iterrows():
            prediction = self.predict_disease(patient.to_dict())
            results.append(prediction)
        return results

def create_sample_data():
    """Create sample patient data"""
    return pd.DataFrame({
        'age': [45, 50, 35, 60, 40],
        'gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'bmi': [25.5, 28.2, 22.1, 30.5, 26.8],
        'systolic_bp': [120, 140, 110, 160, 130],
        'diastolic_bp': [80, 90, 70, 100, 85],
        'heart_rate': [70, 85, 65, 95, 75],
        'glucose': [100, 120, 90, 150, 110],
        'cholesterol': [200, 250, 180, 300, 220],
        'hdl_cholesterol': [50, 45, 55, 40, 48],
        'ldl_cholesterol': [120, 150, 100, 200, 130],
        'triglycerides': [150, 200, 120, 250, 170],
        'smoking': [0, 1, 0, 1, 0],
        'alcohol_consumption': [1, 2, 0, 3, 1],
        'exercise_frequency': [2, 1, 3, 0, 2],
        'diet_quality': [3, 2, 4, 1, 3],
        'family_diabetes': [0, 1, 0, 1, 0],
        'family_heart_disease': [0, 0, 1, 1, 0],
        'family_eye_disease': [0, 0, 1, 0, 0],
        'hypertension': [0, 1, 0, 1, 0],
        'previous_stroke': [0, 0, 0, 1, 0],
        'kidney_disease': [0, 0, 0, 0, 0]
    })

def visualize_predictions(results):
    """Visualize prediction results"""
    diseases = ['diabetes', 'heart_disease', 'eye_disease']
    risk_scores = {disease: [] for disease in diseases}
    
    for result in results:
        for disease in diseases:
            risk_scores[disease].append(result[disease]['risk_score'])
    
    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, disease in enumerate(diseases):
        axes[i].hist(risk_scores[disease], bins=10, alpha=0.7)
        axes[i].set_title(f'{disease.replace("_", " ").title()} Risk Distribution')
        axes[i].set_xlabel('Risk Score')
        axes[i].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Initialize client
    client = HealthcareClient()
    
    # Check health
    print("API Health:", client.get_health_status())
    
    # Get model info
    print("Model Info:", client.get_model_info())
    
    # Create sample data
    patients = create_sample_data()
    print(f"Created {len(patients)} sample patients")
    
    # Get predictions
    results = client.batch_predict(patients)
    
    # Display results
    for i, result in enumerate(results):
        print(f"\nPatient {i+1} Predictions:")
        for disease, risk in result.items():
            print(f"  {disease}: {risk['risk_level']} ({risk['risk_score']:.2f})")
    
    # Visualize results
    visualize_predictions(results)
