"""
Tests for ML models module
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_models import HealthcareMLPipeline


class TestHealthcareMLPipeline:
    """Test cases for HealthcareMLPipeline class"""
    
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
            'family_heart_disease': [1, 0, 0, 1],
            'family_eye_disease': [0, 0, 1, 0],
            'hypertension': [0, 1, 0, 1],
            'previous_stroke': [0, 0, 0, 1],
            'kidney_disease': [0, 0, 0, 0],
            'chest_pain_type': ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'],
            'exercise_angina': [0, 1, 0, 1],
            'st_depression': [0.0, 1.5, 0.0, 2.0],
            'major_vessels': [0, 1, 0, 2],
            'thalassemia': ['Normal', 'Fixed Defect', 'Normal', 'Reversible Defect']
        })
    
    @pytest.fixture
    def ml_pipeline(self):
        """Create ML pipeline instance for testing"""
        return HealthcareMLPipeline()
    
    def test_initialization(self, ml_pipeline):
        """Test ML pipeline initialization"""
        assert ml_pipeline.models == {}
        assert ml_pipeline.model_path == 'models/'
        assert hasattr(ml_pipeline, 'preprocessor')
    
    @patch('os.makedirs')
    def test_model_path_creation(self, mock_makedirs, ml_pipeline):
        """Test that model path is created"""
        mock_makedirs.assert_called_once_with('models/', exist_ok=True)
    
    def test_load_models_no_files(self, ml_pipeline):
        """Test loading models when no model files exist"""
        with patch('os.path.exists', return_value=False):
            result = ml_pipeline.load_models()
            assert result == False
    
    @patch('joblib.load')
    @patch('os.path.exists')
    def test_load_models_success(self, mock_exists, mock_load, ml_pipeline):
        """Test successful model loading"""
        mock_exists.return_value = True
        mock_model = Mock()
        mock_load.return_value = mock_model
        
        result = ml_pipeline.load_models()
        assert result == True
        assert len(ml_pipeline.models) == 3
    
    def test_predict_diabetes_no_model(self, ml_pipeline, sample_data):
        """Test diabetes prediction when no model is loaded"""
        with pytest.raises(ValueError, match="Diabetes model not loaded"):
            ml_pipeline.predict_diabetes(sample_data.iloc[0])
    
    @patch.object(HealthcareMLPipeline, 'preprocessor')
    def test_predict_diabetes_success(self, mock_preprocessor, ml_pipeline, sample_data):
        """Test successful diabetes prediction"""
        # Mock the model
        mock_model = Mock()
        mock_model.predict_proba.return_value = np.array([[0.2, 0.8]])
        ml_pipeline.models['diabetes'] = mock_model
        
        # Mock the preprocessor
        mock_preprocessor.transform_new_data.return_value = np.array([[1, 2, 3]])
        
        result = ml_pipeline.predict_diabetes(sample_data.iloc[0])
        
        assert 'risk_score' in result
        assert 'risk_level' in result
        assert result['risk_score'] == 0.8
        assert result['risk_level'] == 'High'
    
    def test_predict_heart_disease_no_model(self, ml_pipeline, sample_data):
        """Test heart disease prediction when no model is loaded"""
        with pytest.raises(ValueError, match="Heart disease model not loaded"):
            ml_pipeline.predict_heart_disease(sample_data.iloc[0])
    
    def test_predict_eye_disease_no_model(self, ml_pipeline, sample_data):
        """Test eye disease prediction when no model is loaded"""
        with pytest.raises(ValueError, match="Eye disease model not loaded"):
            ml_pipeline.predict_eye_disease(sample_data.iloc[0])
    
    def test_get_model_info_no_models(self, ml_pipeline):
        """Test getting model info when no models are loaded"""
        info = ml_pipeline.get_model_info()
        assert info == {
            'diabetes': {'status': 'Not loaded', 'accuracy': None},
            'heart_disease': {'status': 'Not loaded', 'accuracy': None},
            'eye_disease': {'status': 'Not loaded', 'accuracy': None}
        }
    
    def test_get_model_info_with_models(self, ml_pipeline):
        """Test getting model info when models are loaded"""
        # Mock models with accuracy attributes
        mock_model = Mock()
        mock_model.accuracy = 0.95
        ml_pipeline.models = {
            'diabetes': mock_model,
            'heart_disease': mock_model,
            'eye_disease': mock_model
        }
        
        info = ml_pipeline.get_model_info()
        assert info['diabetes']['status'] == 'Loaded'
        assert info['diabetes']['accuracy'] == 0.95
    
    def test_risk_level_calculation(self, ml_pipeline):
        """Test risk level calculation"""
        # Test low risk
        assert ml_pipeline._calculate_risk_level(0.2) == 'Low'
        
        # Test medium risk
        assert ml_pipeline._calculate_risk_level(0.5) == 'Medium'
        
        # Test high risk
        assert ml_pipeline._calculate_risk_level(0.8) == 'High'
    
    def test_risk_level_boundaries(self, ml_pipeline):
        """Test risk level boundary conditions"""
        # Test exact boundaries
        assert ml_pipeline._calculate_risk_level(0.3) == 'Low'
        assert ml_pipeline._calculate_risk_level(0.31) == 'Medium'
        assert ml_pipeline._calculate_risk_level(0.7) == 'Medium'
        assert ml_pipeline._calculate_risk_level(0.71) == 'High'
    
    @pytest.mark.slow
    def test_model_training_integration(self, ml_pipeline, sample_data):
        """Integration test for model training"""
        # This test would require actual model training
        # Marked as slow to avoid running in quick test suites
        pass
