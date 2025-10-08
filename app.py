from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from ml_models import HealthcareMLPipeline
from data_preprocessing import HealthDataPreprocessor
import os
from config import Config

app = Flask(__name__)
CORS(app, origins=Config.CORS_ORIGINS)

# Initialize ML pipeline
ml_pipeline = HealthcareMLPipeline()

# Load models if they exist
if os.path.exists('models/'):
    try:
        ml_pipeline.load_models()
        print("Models loaded successfully")
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Training new models...")
        ml_pipeline.train_all_models()
else:
    print("No models found. Training new models...")
    ml_pipeline.train_all_models()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Healthcare Assistant API is running',
        'models_loaded': len(ml_pipeline.models) > 0
    })

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    """Predict diabetes risk for a patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp',
            'glucose', 'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol',
            'triglycerides', 'smoking', 'alcohol_consumption', 'exercise_frequency',
            'diet_quality', 'family_diabetes', 'hypertension'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([data])
        
        # Make prediction
        prediction = ml_pipeline.predict_diabetes_risk(patient_data)
        
        return jsonify({
            'disease': 'diabetes',
            'prediction': prediction,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predict/heart', methods=['POST'])
def predict_heart_disease():
    """Predict heart disease risk for a patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
            'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
            'family_heart_disease', 'hypertension'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([data])
        
        # Make prediction
        prediction = ml_pipeline.predict_heart_disease_risk(patient_data)
        
        return jsonify({
            'disease': 'heart_disease',
            'prediction': prediction,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predict/eye', methods=['POST'])
def predict_eye_disease():
    """Predict eye disease risk for a patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose',
            'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
            'family_eye_disease', 'hypertension', 'diabetes_risk'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([data])
        
        # Make prediction
        prediction = ml_pipeline.predict_eye_disease_risk(patient_data)
        
        return jsonify({
            'disease': 'eye_disease',
            'prediction': prediction,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predict/all', methods=['POST'])
def predict_all_diseases():
    """Predict risk for all diseases"""
    try:
        data = request.get_json()
        
        # Validate basic required fields
        basic_fields = [
            'age', 'gender', 'bmi', 'systolic_bp', 'diastolic_bp',
            'glucose', 'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol',
            'triglycerides', 'smoking', 'alcohol_consumption', 'exercise_frequency',
            'diet_quality', 'hypertension'
        ]
        
        missing_fields = [field for field in basic_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Add default values for missing optional fields
        data.setdefault('heart_rate', 75)
        data.setdefault('family_diabetes', 0)
        data.setdefault('family_heart_disease', 0)
        data.setdefault('family_eye_disease', 0)
        data.setdefault('previous_stroke', 0)
        data.setdefault('kidney_disease', 0)
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([data])
        
        # Make predictions for all diseases
        predictions = {}
        
        # Diabetes prediction
        try:
            diabetes_pred = ml_pipeline.predict_diabetes_risk(patient_data)
            predictions['diabetes'] = diabetes_pred
        except Exception as e:
            predictions['diabetes'] = {'error': str(e)}
        
        # Heart disease prediction
        try:
            heart_pred = ml_pipeline.predict_heart_disease_risk(patient_data)
            predictions['heart_disease'] = heart_pred
        except Exception as e:
            predictions['heart_disease'] = {'error': str(e)}
        
        # Eye disease prediction (need diabetes risk first)
        try:
            if 'diabetes' in predictions and 'error' not in predictions['diabetes']:
                patient_data['diabetes_risk'] = predictions['diabetes']['risk_score']
            else:
                patient_data['diabetes_risk'] = 0.5  # Default value
            
            eye_pred = ml_pipeline.predict_eye_disease_risk(patient_data)
            predictions['eye_disease'] = eye_pred
        except Exception as e:
            predictions['eye_disease'] = {'error': str(e)}
        
        return jsonify({
            'predictions': predictions,
            'timestamp': pd.Timestamp.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/models/info', methods=['GET'])
def get_models_info():
    """Get information about loaded models"""
    model_info = {}
    
    for disease_type, model in ml_pipeline.models.items():
        model_info[disease_type] = {
            'type': type(model).__name__,
            'loaded': True,
            'feature_count': len(ml_pipeline.preprocessor.feature_columns.get(disease_type, []))
        }
    
    return jsonify({
        'models': model_info,
        'total_models': len(ml_pipeline.models)
    })

@app.route('/models/retrain', methods=['POST'])
def retrain_models():
    """Retrain all models with new data"""
    try:
        data = request.get_json()
        n_samples = data.get('n_samples', 10000)
        
        # Train new models
        results = ml_pipeline.train_all_models(n_samples=n_samples)
        
        return jsonify({
            'message': 'Models retrained successfully',
            'results': {
                disease: {
                    model_name: {
                        'auc_score': result['auc_score']
                    } for model_name, result in models.items()
                } for disease, models in results.items()
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Retraining failed: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Healthcare Assistant API...")
    print(f"Models loaded: {list(ml_pipeline.models.keys())}")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
