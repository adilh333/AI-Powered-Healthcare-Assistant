import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Azure Configuration
    AZURE_SUBSCRIPTION_ID = os.environ.get('AZURE_SUBSCRIPTION_ID')
    AZURE_RESOURCE_GROUP = os.environ.get('AZURE_RESOURCE_GROUP', 'healthcare-assistant-rg')
    AZURE_WORKSPACE_NAME = os.environ.get('AZURE_WORKSPACE_NAME', 'healthcare-ml-workspace')
    AZURE_STORAGE_ACCOUNT = os.environ.get('AZURE_STORAGE_ACCOUNT')
    AZURE_STORAGE_KEY = os.environ.get('AZURE_STORAGE_KEY')
    
    # Model Configuration
    MODEL_PATH = 'models/'
    DATA_PATH = 'data/'
    
    # API Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Prediction Thresholds
    DIABETES_THRESHOLD = 0.5
    HEART_DISEASE_THRESHOLD = 0.5
    EYE_DISEASE_THRESHOLD = 0.5
