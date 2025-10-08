"""
Tests for data preprocessing module
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_preprocessing import HealthDataPreprocessor


class TestHealthDataPreprocessor:
    """Test cases for HealthDataPreprocessor class"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return pd.DataFrame({
            'age': [45, 50, 35, 60],
            'gender': ['Male', 'Female', 'Male', 'Female'],
            'bmi': [25.5, 28.2, 22.1, 30.5],
            'systolic_bp': [120, 140, 110, 160],
            'diastolic_bp': [80, 90, 70, 100],
            'heart_rate': [70, 85, 65, 95],
            'glucose': [100, 120, 90, 150],
            'cholesterol': [200, 250, 180, 300],
            'hdl_cholesterol': [50, 45, 55, 40],
            'ldl_cholesterol': [120, 150, 100, 200],
            'triglycerides': [150, 200, 120, 250],
            'smoking': [0, 1, 0, 1],
            'alcohol_consumption': [1, 2, 0, 3],
            'exercise_frequency': [2, 1, 3, 0],
            'diet_quality': [3, 2, 4, 1],
            'family_diabetes': [0, 1, 0, 1],
            'family_heart_disease': [0, 0, 1, 1],
            'family_eye_disease': [0, 0, 1, 0],
            'hypertension': [0, 1, 0, 1],
            'previous_stroke': [0, 0, 0, 1],
            'kidney_disease': [0, 0, 0, 0]
        })
    
    @pytest.fixture
    def preprocessor(self):
        """Create preprocessor instance for testing"""
        return HealthDataPreprocessor()
    
    def test_initialization(self, preprocessor):
        """Test preprocessor initialization"""
        assert preprocessor.scalers == {}
        assert preprocessor.feature_columns == {}
        assert preprocessor.label_encoders == {}
    
    def test_create_synthetic_data(self, preprocessor):
        """Test synthetic data creation"""
        data = preprocessor.create_synthetic_data(n_samples=100)
        
        assert len(data) == 100
        assert 'age' in data.columns
        assert 'gender' in data.columns
        assert 'bmi' in data.columns
        assert 'diabetes_risk' in data.columns
        assert 'heart_disease_risk' in data.columns
        assert 'eye_disease_risk' in data.columns
    
    def test_synthetic_data_types(self, preprocessor):
        """Test data types in synthetic data"""
        data = preprocessor.create_synthetic_data(n_samples=50)
        
        # Check numeric columns
        numeric_cols = ['age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate']
        for col in numeric_cols:
            assert pd.api.types.is_numeric_dtype(data[col])
        
        # Check categorical columns
        assert data['gender'].dtype == 'object'
        assert set(data['gender'].unique()).issubset({'Male', 'Female'})
    
    def test_synthetic_data_ranges(self, preprocessor):
        """Test that synthetic data is within reasonable ranges"""
        data = preprocessor.create_synthetic_data(n_samples=100)
        
        # Age should be between 18 and 100
        assert data['age'].min() >= 18
        assert data['age'].max() <= 100
        
        # BMI should be between 15 and 50
        assert data['bmi'].min() >= 15
        assert data['bmi'].max() <= 50
        
        # Blood pressure should be reasonable
        assert data['systolic_bp'].min() >= 80
        assert data['systolic_bp'].max() <= 200
    
    def test_preprocess_for_diabetes(self, preprocessor, sample_data):
        """Test diabetes preprocessing"""
        # Add target column
        sample_data['diabetes_risk'] = [0, 1, 0, 1]
        
        result = preprocessor.preprocess_for_diabetes(sample_data)
        
        assert 'X' in result
        assert 'y' in result
        assert 'scaler' in result
        assert 'feature_columns' in result
        
        # Check that features are scaled
        X = result['X']
        assert X.shape[0] == len(sample_data)
        assert X.shape[1] > 0
    
    def test_preprocess_for_heart_disease(self, preprocessor, sample_data):
        """Test heart disease preprocessing"""
        # Add target column
        sample_data['heart_disease_risk'] = [0, 1, 0, 1]
        
        result = preprocessor.preprocess_for_heart_disease(sample_data)
        
        assert 'X' in result
        assert 'y' in result
        assert 'scaler' in result
        assert 'feature_columns' in result
    
    def test_preprocess_for_eye_disease(self, preprocessor, sample_data):
        """Test eye disease preprocessing"""
        # Add target column
        sample_data['eye_disease_risk'] = [0, 1, 0, 1]
        sample_data['diabetes_risk'] = [0, 1, 0, 1]  # Required for eye disease
        
        result = preprocessor.preprocess_for_eye_disease(sample_data)
        
        assert 'X' in result
        assert 'y' in result
        assert 'scaler' in result
        assert 'feature_columns' in result
    
    def test_transform_new_data(self, preprocessor, sample_data):
        """Test transforming new data"""
        # First, set up a mock scaler and feature columns
        preprocessor.scalers['diabetes'] = Mock()
        preprocessor.scalers['diabetes'].transform.return_value = np.array([[1, 2, 3]])
        preprocessor.feature_columns['diabetes'] = ['age', 'bmi', 'glucose']
        
        result = preprocessor.transform_new_data(sample_data, 'diabetes')
        
        assert result.shape[1] == 3  # Should match number of features
        preprocessor.scalers['diabetes'].transform.assert_called_once()
    
    def test_transform_new_data_missing_scaler(self, preprocessor, sample_data):
        """Test transform_new_data when scaler is missing"""
        with pytest.raises(ValueError, match="No scaler found for diabetes"):
            preprocessor.transform_new_data(sample_data, 'diabetes')
    
    def test_save_preprocessors(self, preprocessor):
        """Test saving preprocessors"""
        # Set up mock data
        preprocessor.scalers['diabetes'] = Mock()
        preprocessor.feature_columns['diabetes'] = ['age', 'bmi']
        
        with patch('joblib.dump') as mock_dump:
            preprocessor.save_preprocessors('test_models/')
            
            # Check that dump was called for scaler and feature columns
            assert mock_dump.call_count >= 2
    
    def test_load_preprocessors(self, preprocessor):
        """Test loading preprocessors"""
        with patch('joblib.load') as mock_load:
            mock_load.return_value = ['age', 'bmi']
            
            result = preprocessor.load_preprocessors('test_models/')
            
            assert result == True
            assert 'diabetes' in preprocessor.feature_columns
    
    def test_load_preprocessors_file_not_found(self, preprocessor):
        """Test loading preprocessors when files don't exist"""
        with patch('os.path.exists', return_value=False):
            result = preprocessor.load_preprocessors('nonexistent/')
            assert result == False
    
    def test_estimate_diabetes_risk(self, preprocessor, sample_data):
        """Test diabetes risk estimation"""
        risk = preprocessor._estimate_diabetes_risk(sample_data.iloc[0])
        
        assert 0 <= risk <= 1
        assert isinstance(risk, (int, float))
    
    def test_estimate_eye_disease_risk(self, preprocessor, sample_data):
        """Test eye disease risk estimation"""
        risk = preprocessor._estimate_eye_disease_risk(sample_data.iloc[0])
        
        assert 0 <= risk <= 1
        assert isinstance(risk, (int, float))
    
    def test_gender_encoding(self, preprocessor):
        """Test gender encoding in transform_new_data"""
        # Create data with gender column
        data = pd.DataFrame({
            'age': [45],
            'gender': ['Male'],
            'bmi': [25.5]
        })
        
        # Set up mock scaler
        preprocessor.scalers['diabetes'] = Mock()
        preprocessor.scalers['diabetes'].transform.return_value = np.array([[1, 2, 3]])
        preprocessor.feature_columns['diabetes'] = ['age', 'bmi', 'gender_encoded']
        
        result = preprocessor.transform_new_data(data, 'diabetes')
        
        # Should not raise an error and should handle gender encoding
        assert result.shape[1] == 3
