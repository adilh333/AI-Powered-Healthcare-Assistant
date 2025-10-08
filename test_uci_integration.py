#!/usr/bin/env python3
"""
Test script for UCI Heart Disease Dataset integration
"""

import pandas as pd
import numpy as np
from data_loader import UCIHeartDiseaseLoader
from data_preprocessing import HealthDataPreprocessor
from ml_models import HealthcareMLPipeline

def test_data_loading():
    """Test UCI dataset loading and processing"""
    print("🧪 Testing UCI Heart Disease Dataset Integration")
    print("=" * 60)
    
    # Test data loader
    print("1. Testing UCI data loader...")
    loader = UCIHeartDiseaseLoader()
    
    # Download data
    if loader.download_data():
        print("   ✅ Dataset downloaded successfully")
    else:
        print("   ❌ Failed to download dataset")
        return False
    
    # Load and clean data
    df = loader.load_and_clean_data()
    if df is not None:
        print(f"   ✅ Data loaded: {len(df)} records, {len(df.columns)} features")
        print(f"   📊 Target distribution: {df['target'].value_counts().to_dict()}")
    else:
        print("   ❌ Failed to load and clean data")
        return False
    
    # Test extended dataset creation
    print("\n2. Testing extended dataset creation...")
    extended_df = loader.create_extended_dataset(df, n_samples=1000)
    print(f"   ✅ Extended dataset created: {len(extended_df)} records")
    
    # Test preprocessing
    print("\n3. Testing data preprocessing...")
    preprocessor = HealthDataPreprocessor()
    mapped_df = preprocessor._map_uci_to_standard_format(extended_df)
    print(f"   ✅ Data mapped to standard format: {len(mapped_df)} records")
    print(f"   📊 Features: {list(mapped_df.columns)}")
    
    return True

def test_ml_training():
    """Test ML model training with UCI data"""
    print("\n4. Testing ML model training...")
    
    try:
        pipeline = HealthcareMLPipeline()
        results = pipeline.train_all_models(n_samples=1000, use_real_data=True)
        
        print("   ✅ ML models trained successfully")
        
        # Print results
        for disease, models in results.items():
            print(f"   📈 {disease.replace('_', ' ').title()}:")
            for model_name, result in models.items():
                print(f"      {model_name}: AUC = {result['auc_score']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ML training failed: {e}")
        return False

def test_prediction():
    """Test prediction with sample data"""
    print("\n5. Testing prediction with sample data...")
    
    try:
        pipeline = HealthcareMLPipeline()
        pipeline.load_models()
        
        # Create sample patient data
        sample_data = pd.DataFrame([{
            'age': 55,
            'gender': 'Male',
            'bmi': 28.5,
            'systolic_bp': 140,
            'diastolic_bp': 90,
            'heart_rate': 150,
            'glucose': 120,
            'cholesterol': 250,
            'hdl_cholesterol': 40,
            'ldl_cholesterol': 180,
            'triglycerides': 200,
            'smoking': 1,
            'alcohol_consumption': 1,
            'exercise_frequency': 1,
            'diet_quality': 2,
            'family_diabetes': 1,
            'family_heart_disease': 1,
            'family_eye_disease': 0,
            'hypertension': 1,
            'previous_stroke': 0,
            'kidney_disease': 0,
            'chest_pain_type': 'Atypical Angina',
            'exercise_angina': 1,
            'st_depression': 1.5,
            'major_vessels': 2,
            'thalassemia': 'Fixed Defect'
        }])
        
        # Test predictions
        diabetes_pred = pipeline.predict_diabetes_risk(sample_data)
        heart_pred = pipeline.predict_heart_disease_risk(sample_data)
        
        print(f"   ✅ Diabetes prediction: {diabetes_pred['risk_score']:.3f} ({diabetes_pred['risk_level']})")
        print(f"   ✅ Heart disease prediction: {heart_pred['risk_score']:.3f} ({heart_pred['risk_level']})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Prediction failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏥 Healthcare Assistant - UCI Dataset Integration Test")
    print("=" * 60)
    
    # Run tests
    tests = [
        test_data_loading,
        test_ml_training,
        test_prediction
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    # Summary
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! UCI dataset integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
