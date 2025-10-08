"""
Azure Functions for Healthcare Assistant API
"""
import logging
import json
import os
import joblib
import pandas as pd
import numpy as np
from azure.functions import HttpRequest, HttpResponse
from data_preprocessing import HealthDataPreprocessor
from ml_models import HealthcareMLPipeline

# Initialize ML pipeline
ml_pipeline = HealthcareMLPipeline()

def main(req: HttpRequest) -> HttpResponse:
    """Main Azure Function entry point"""
    logging.info('Healthcare Assistant function processed a request.')
    
    try:
        # Get request method and route
        method = req.method
        route = req.route_params.get('route', '')
        
        if method == 'GET' and route == 'health':
            return health_check()
        elif method == 'POST' and route == 'predict':
            return predict_disease(req)
        elif method == 'GET' and route == 'models':
            return get_models_info()
        else:
            return HttpResponse(
                json.dumps({'error': 'Endpoint not found'}),
                status_code=404,
                mimetype='application/json'
            )
            
    except Exception as e:
        logging.error(f'Error processing request: {str(e)}')
        return HttpResponse(
            json.dumps({'error': f'Internal server error: {str(e)}'}),
            status_code=500,
            mimetype='application/json'
        )

def health_check():
    """Health check endpoint"""
    return HttpResponse(
        json.dumps({
            'status': 'healthy',
            'message': 'Healthcare Assistant API is running on Azure Functions',
            'models_loaded': len(ml_pipeline.models) > 0
        }),
        status_code=200,
        mimetype='application/json'
    )

def predict_disease(req: HttpRequest):
    """Predict disease risk"""
    try:
        # Parse request body
        req_body = req.get_json()
        if not req_body:
            return HttpResponse(
                json.dumps({'error': 'No JSON data provided'}),
                status_code=400,
                mimetype='application/json'
            )
        
        # Get disease type from query parameters
        disease_type = req.params.get('type', 'all')
        
        # Convert to DataFrame
        patient_data = pd.DataFrame([req_body])
        
        predictions = {}
        
        if disease_type == 'all' or disease_type == 'diabetes':
            try:
                diabetes_pred = ml_pipeline.predict_diabetes_risk(patient_data)
                predictions['diabetes'] = diabetes_pred
            except Exception as e:
                predictions['diabetes'] = {'error': str(e)}
        
        if disease_type == 'all' or disease_type == 'heart':
            try:
                heart_pred = ml_pipeline.predict_heart_disease_risk(patient_data)
                predictions['heart_disease'] = heart_pred
            except Exception as e:
                predictions['heart_disease'] = {'error': str(e)}
        
        if disease_type == 'all' or disease_type == 'eye':
            try:
                # Add diabetes risk if available
                if 'diabetes' in predictions and 'error' not in predictions['diabetes']:
                    patient_data['diabetes_risk'] = predictions['diabetes']['risk_score']
                else:
                    patient_data['diabetes_risk'] = 0.5
                
                eye_pred = ml_pipeline.predict_eye_disease_risk(patient_data)
                predictions['eye_disease'] = eye_pred
            except Exception as e:
                predictions['eye_disease'] = {'error': str(e)}
        
        return HttpResponse(
            json.dumps({
                'predictions': predictions,
                'timestamp': pd.Timestamp.now().isoformat()
            }),
            status_code=200,
            mimetype='application/json'
        )
        
    except Exception as e:
        return HttpResponse(
            json.dumps({'error': f'Prediction failed: {str(e)}'}),
            status_code=500,
            mimetype='application/json'
        )

def get_models_info():
    """Get information about loaded models"""
    model_info = {}
    
    for disease_type, model in ml_pipeline.models.items():
        model_info[disease_type] = {
            'type': type(model).__name__,
            'loaded': True,
            'feature_count': len(ml_pipeline.preprocessor.feature_columns.get(disease_type, []))
        }
    
    return HttpResponse(
        json.dumps({
            'models': model_info,
            'total_models': len(ml_pipeline.models)
        }),
        status_code=200,
        mimetype='application/json'
    )
