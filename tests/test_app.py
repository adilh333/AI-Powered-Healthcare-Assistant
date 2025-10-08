"""
Tests for Flask API application
"""

import pytest
import json
from unittest.mock import Mock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


class TestFlaskAPI:
    """Test cases for Flask API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_models_info_endpoint(self, client):
        """Test models info endpoint"""
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.get_model_info.return_value = {
                'diabetes': {'status': 'Loaded', 'accuracy': 0.95},
                'heart_disease': {'status': 'Loaded', 'accuracy': 0.98},
                'eye_disease': {'status': 'Loaded', 'accuracy': 0.92}
            }
            
            response = client.get('/models/info')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert 'diabetes' in data
            assert 'heart_disease' in data
            assert 'eye_disease' in data
    
    def test_predict_diabetes_endpoint(self, client):
        """Test diabetes prediction endpoint"""
        test_data = {
            'age': 45,
            'gender': 'Male',
            'bmi': 25.5,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'heart_rate': 70,
            'glucose': 100,
            'cholesterol': 200,
            'hdl_cholesterol': 50,
            'ldl_cholesterol': 120,
            'triglycerides': 150,
            'smoking': 0,
            'alcohol_consumption': 1,
            'exercise_frequency': 2,
            'diet_quality': 3,
            'family_diabetes': 0,
            'family_heart_disease': 0,
            'family_eye_disease': 0,
            'hypertension': 0,
            'previous_stroke': 0,
            'kidney_disease': 0
        }
        
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.predict_diabetes.return_value = {
                'risk_score': 0.3,
                'risk_level': 'Low'
            }
            
            response = client.post('/predict/diabetes', 
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'risk_score' in data
            assert 'risk_level' in data
    
    def test_predict_heart_disease_endpoint(self, client):
        """Test heart disease prediction endpoint"""
        test_data = {
            'age': 50,
            'gender': 'Female',
            'bmi': 28.2,
            'systolic_bp': 140,
            'diastolic_bp': 90,
            'heart_rate': 85,
            'cholesterol': 250,
            'hdl_cholesterol': 45,
            'ldl_cholesterol': 150,
            'triglycerides': 200,
            'smoking': 1,
            'alcohol_consumption': 2,
            'exercise_frequency': 1,
            'diet_quality': 2,
            'family_heart_disease': 1,
            'hypertension': 1,
            'previous_stroke': 0,
            'kidney_disease': 0,
            'chest_pain_type': 'Atypical Angina',
            'exercise_angina': 1,
            'st_depression': 1.5,
            'major_vessels': 1,
            'thalassemia': 'Fixed Defect'
        }
        
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.predict_heart_disease.return_value = {
                'risk_score': 0.8,
                'risk_level': 'High'
            }
            
            response = client.post('/predict/heart_disease',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'risk_score' in data
            assert 'risk_level' in data
    
    def test_predict_eye_disease_endpoint(self, client):
        """Test eye disease prediction endpoint"""
        test_data = {
            'age': 60,
            'gender': 'Male',
            'bmi': 30.5,
            'systolic_bp': 160,
            'diastolic_bp': 100,
            'heart_rate': 95,
            'glucose': 150,
            'cholesterol': 300,
            'hdl_cholesterol': 40,
            'ldl_cholesterol': 200,
            'triglycerides': 250,
            'smoking': 1,
            'alcohol_consumption': 3,
            'exercise_frequency': 0,
            'diet_quality': 1,
            'family_eye_disease': 1,
            'hypertension': 1,
            'previous_stroke': 1,
            'kidney_disease': 0
        }
        
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.predict_eye_disease.return_value = {
                'risk_score': 0.7,
                'risk_level': 'High'
            }
            
            response = client.post('/predict/eye_disease',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'risk_score' in data
            assert 'risk_level' in data
    
    def test_predict_all_endpoint(self, client):
        """Test predict all diseases endpoint"""
        test_data = {
            'age': 45,
            'gender': 'Male',
            'bmi': 25.5,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'heart_rate': 70,
            'glucose': 100,
            'cholesterol': 200,
            'hdl_cholesterol': 50,
            'ldl_cholesterol': 120,
            'triglycerides': 150,
            'smoking': 0,
            'alcohol_consumption': 1,
            'exercise_frequency': 2,
            'diet_quality': 3,
            'family_diabetes': 0,
            'family_heart_disease': 0,
            'family_eye_disease': 0,
            'hypertension': 0,
            'previous_stroke': 0,
            'kidney_disease': 0
        }
        
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.predict_diabetes.return_value = {
                'risk_score': 0.3, 'risk_level': 'Low'
            }
            mock_pipeline.predict_heart_disease.return_value = {
                'risk_score': 0.2, 'risk_level': 'Low'
            }
            mock_pipeline.predict_eye_disease.return_value = {
                'risk_score': 0.1, 'risk_level': 'Low'
            }
            
            response = client.post('/predict/all',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'diabetes' in data
            assert 'heart_disease' in data
            assert 'eye_disease' in data
    
    def test_invalid_json_request(self, client):
        """Test handling of invalid JSON"""
        response = client.post('/predict/diabetes',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        incomplete_data = {'age': 45}  # Missing required fields
        
        response = client.post('/predict/diabetes',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        # Should handle gracefully - either return error or use defaults
        assert response.status_code in [200, 400]
    
    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get('/health')
        assert 'Access-Control-Allow-Origin' in response.headers
    
    def test_error_handling(self, client):
        """Test error handling in prediction endpoints"""
        with patch('app.ml_pipeline') as mock_pipeline:
            mock_pipeline.predict_diabetes.side_effect = Exception("Model error")
            
            test_data = {'age': 45, 'gender': 'Male', 'bmi': 25.5}
            response = client.post('/predict/diabetes',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
