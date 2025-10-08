"""
Simplified Vercel API for Healthcare Assistant
This version works without requiring the full ML pipeline initially
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        "message": "AI-Powered Healthcare Assistant API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict_diabetes": "/predict/diabetes",
            "predict_heart_disease": "/predict/heart_disease", 
            "predict_eye_disease": "/predict/eye_disease",
            "predict_all": "/predict/all"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Healthcare Assistant API is running",
        "version": "1.0.0"
    })

@app.route('/predict/diabetes', methods=['POST'])
def predict_diabetes():
    """Predict diabetes risk (simplified version)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Simple risk calculation based on basic factors
        age = data.get('age', 50)
        bmi = data.get('bmi', 25)
        glucose = data.get('glucose', 100)
        
        # Simple scoring system
        score = 0
        if age > 45: score += 1
        if bmi > 25: score += 1
        if glucose > 126: score += 1
        
        # Determine risk level
        if score >= 2:
            risk_level = "High"
            probability = random.uniform(0.7, 0.9)
        elif score == 1:
            risk_level = "Medium"
            probability = random.uniform(0.3, 0.6)
        else:
            risk_level = "Low"
            probability = random.uniform(0.1, 0.3)
        
        return jsonify({
            "disease": "diabetes",
            "risk_level": risk_level,
            "probability": probability,
            "recommendation": _get_diabetes_recommendation(risk_level)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/heart_disease', methods=['POST'])
def predict_heart_disease():
    """Predict heart disease risk (simplified version)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Simple risk calculation
        age = data.get('age', 50)
        systolic_bp = data.get('systolic_bp', 120)
        cholesterol = data.get('cholesterol', 200)
        
        score = 0
        if age > 50: score += 1
        if systolic_bp > 140: score += 1
        if cholesterol > 240: score += 1
        
        if score >= 2:
            risk_level = "High"
            probability = random.uniform(0.6, 0.8)
        elif score == 1:
            risk_level = "Medium"
            probability = random.uniform(0.3, 0.5)
        else:
            risk_level = "Low"
            probability = random.uniform(0.1, 0.3)
        
        return jsonify({
            "disease": "heart_disease",
            "risk_level": risk_level,
            "probability": probability,
            "recommendation": _get_heart_disease_recommendation(risk_level)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/eye_disease', methods=['POST'])
def predict_eye_disease():
    """Predict eye disease risk (simplified version)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Simple risk calculation
        age = data.get('age', 50)
        glucose = data.get('glucose', 100)
        
        score = 0
        if age > 60: score += 1
        if glucose > 140: score += 1
        
        if score >= 1:
            risk_level = "Medium"
            probability = random.uniform(0.4, 0.6)
        else:
            risk_level = "Low"
            probability = random.uniform(0.1, 0.3)
        
        return jsonify({
            "disease": "eye_disease",
            "risk_level": risk_level,
            "probability": probability,
            "recommendation": _get_eye_disease_recommendation(risk_level)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/all', methods=['POST'])
def predict_all():
    """Predict all disease risks"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        results = {}
        
        # Get predictions from each endpoint
        diabetes_result = predict_diabetes().get_json()
        heart_result = predict_heart_disease().get_json()
        eye_result = predict_eye_disease().get_json()
        
        results['diabetes'] = diabetes_result
        results['heart_disease'] = heart_result
        results['eye_disease'] = eye_result
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def _get_diabetes_recommendation(risk_level):
    """Get diabetes recommendations"""
    if risk_level == "High":
        return "Consult with a healthcare provider immediately. Consider lifestyle changes including diet modification and regular exercise."
    elif risk_level == "Medium":
        return "Monitor your blood sugar regularly and maintain a healthy lifestyle. Consider annual check-ups."
    else:
        return "Continue maintaining a healthy lifestyle with balanced diet and regular exercise."

def _get_heart_disease_recommendation(risk_level):
    """Get heart disease recommendations"""
    if risk_level == "High":
        return "Schedule a consultation with a cardiologist. Monitor blood pressure and cholesterol regularly."
    elif risk_level == "Medium":
        return "Maintain heart-healthy habits: regular exercise, low-sodium diet, and stress management."
    else:
        return "Continue heart-healthy lifestyle practices and regular health check-ups."

def _get_eye_disease_recommendation(risk_level):
    """Get eye disease recommendations"""
    if risk_level == "Medium":
        return "Schedule regular eye examinations and monitor blood sugar levels if diabetic."
    else:
        return "Continue regular eye check-ups and maintain overall health."

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    app.run(debug=True)
