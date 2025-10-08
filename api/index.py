"""
Vercel serverless function for Healthcare Assistant API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Import your ML pipeline
try:
    from ml_models import HealthcareMLPipeline
    from data_preprocessing import HealthDataPreprocessor
    
    # Initialize ML pipeline
    ml_pipeline = HealthcareMLPipeline()
    ml_pipeline.load_models()
    
    print("✅ ML models loaded successfully for Vercel")
except Exception as e:
    print(f"❌ Error loading ML models: {e}")
    ml_pipeline = None

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "AI-Powered Healthcare Assistant API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "models": "/models/info", 
            "predict_diabetes": "/predict/diabetes",
            "predict_heart_disease": "/predict/heart_disease",
            "predict_eye_disease": "/predict/eye_disease",
            "predict_all": "/predict/all"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        models_loaded = len(ml_pipeline.models) if ml_pipeline else 0
        return jsonify({
            "status": "healthy",
            "models_loaded": models_loaded,
            "timestamp": str(pd.Timestamp.now())
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/models/info', methods=['GET'])
def models_info():
    """Get information about loaded models"""
    try:
        if not ml_pipeline:
            return jsonify({"error": "ML pipeline not loaded"}), 500
        
        info = ml_pipeline.get_model_info()
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    """Predict diabetes risk"""
    try:
        if not ml_pipeline:
            return jsonify({"error": "ML pipeline not loaded"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add default values for missing UCI-specific features
        data = _add_default_values(data)
        
        result = ml_pipeline.predict_diabetes(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/heart_disease', methods=['POST'])
def predict_heart_disease():
    """Predict heart disease risk"""
    try:
        if not ml_pipeline:
            return jsonify({"error": "ML pipeline not loaded"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add default values for missing UCI-specific features
        data = _add_default_values(data)
        
        result = ml_pipeline.predict_heart_disease(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/eye_disease', methods=['POST'])
def predict_eye_disease():
    """Predict eye disease risk"""
    try:
        if not ml_pipeline:
            return jsonify({"error": "ML pipeline not loaded"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add default values for missing UCI-specific features
        data = _add_default_values(data)
        
        result = ml_pipeline.predict_eye_disease(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/all', methods=['POST'])
def predict_all():
    """Predict all disease risks"""
    try:
        if not ml_pipeline:
            return jsonify({"error": "ML pipeline not loaded"}), 500
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Add default values for missing UCI-specific features
        data = _add_default_values(data)
        
        results = {}
        
        try:
            results['diabetes'] = ml_pipeline.predict_diabetes(data)
        except Exception as e:
            results['diabetes'] = {"error": str(e)}
        
        try:
            results['heart_disease'] = ml_pipeline.predict_heart_disease(data)
        except Exception as e:
            results['heart_disease'] = {"error": str(e)}
        
        try:
            results['eye_disease'] = ml_pipeline.predict_eye_disease(data)
        except Exception as e:
            results['eye_disease'] = {"error": str(e)}
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _add_default_values(data):
    """Add default values for UCI-specific features if missing"""
    defaults = {
        'chest_pain_type': 'Typical Angina',
        'exercise_angina': 0,
        'st_depression': 0.0,
        'major_vessels': 0,
        'thalassemia': 'Normal'
    }
    
    for key, value in defaults.items():
        if key not in data:
            data[key] = value
    
    return data

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
