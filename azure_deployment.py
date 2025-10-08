"""
Azure ML deployment configuration for Healthcare Assistant
"""
import os
import joblib
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Environment, ManagedOnlineEndpoint, ManagedOnlineDeployment
from azure.identity import DefaultAzureCredential
from azure.ai.ml.constants import AssetTypes
import json

class AzureMLDeployment:
    """Handles Azure ML deployment for healthcare models"""
    
    def __init__(self, subscription_id, resource_group, workspace_name):
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.workspace_name = workspace_name
        
        # Initialize ML client
        self.credential = DefaultAzureCredential()
        self.ml_client = MLClient(
            credential=self.credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
    
    def create_environment(self):
        """Create Azure ML environment for the healthcare app"""
        env_docker_image = Environment(
            name="healthcare-env",
            description="Environment for Healthcare Assistant ML models",
            image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest",
            conda_file="conda.yml"
        )
        
        try:
            self.ml_client.environments.create_or_update(env_docker_image)
            print("Environment created successfully")
        except Exception as e:
            print(f"Error creating environment: {e}")
    
    def register_model(self, model_path, model_name):
        """Register ML model in Azure ML"""
        try:
            model = self.ml_client.models.create_or_update(
                name=model_name,
                path=model_path,
                type=AssetTypes.CUSTOM_MODEL,
                description=f"Healthcare {model_name} prediction model"
            )
            print(f"Model {model_name} registered successfully")
            return model
        except Exception as e:
            print(f"Error registering model {model_name}: {e}")
            return None
    
    def create_scoring_script(self):
        """Create scoring script for Azure ML deployment"""
        scoring_script = '''
import json
import joblib
import pandas as pd
import numpy as np
from data_preprocessing import HealthDataPreprocessor

def init():
    """Initialize the model and preprocessor"""
    global model, preprocessor
    
    # Load model and preprocessor
    model = joblib.load("model.pkl")
    preprocessor = HealthDataPreprocessor()
    preprocessor.load_preprocessors()

def run(raw_data):
    """Run prediction on input data"""
    try:
        # Parse input data
        data = json.loads(raw_data)
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Transform data
        X_scaled = preprocessor.transform_new_data(df, 'diabetes')  # Adjust for specific model
        
        # Make prediction
        risk_score = model.predict_proba(X_scaled)[0, 1]
        risk_level = "High" if risk_score > 0.6 else "Medium" if risk_score > 0.3 else "Low"
        
        # Generate recommendations
        recommendations = []
        if risk_score > 0.6:
            recommendations.extend([
                "Schedule regular monitoring",
                "Consult with a specialist",
                "Maintain healthy lifestyle"
            ])
        elif risk_score > 0.3:
            recommendations.extend([
                "Monitor regularly",
                "Maintain healthy diet",
                "Exercise regularly"
            ])
        else:
            recommendations.extend([
                "Continue healthy lifestyle",
                "Regular checkups"
            ])
        
        return {
            "risk_score": float(risk_score),
            "risk_level": risk_level,
            "recommendations": recommendations
        }
        
    except Exception as e:
        return {"error": str(e)}
'''
        
        with open("score.py", "w") as f:
            f.write(scoring_script)
        
        print("Scoring script created")
    
    def create_conda_file(self):
        """Create conda environment file for Azure ML"""
        conda_content = {
            "name": "healthcare-env",
            "channels": ["conda-forge", "defaults"],
            "dependencies": [
                "python=3.8",
                "pip",
                {
                    "pip": [
                        "pandas==2.0.3",
                        "numpy==1.24.3",
                        "scikit-learn==1.3.0",
                        "xgboost==1.7.6",
                        "joblib==1.3.2",
                        "azure-ai-ml==1.10.0",
                        "azure-identity==1.13.0"
                    ]
                }
            ]
        }
        
        with open("conda.yml", "w") as f:
            import yaml
            yaml.dump(conda_content, f, default_flow_style=False)
        
        print("Conda file created")
    
    def deploy_model(self, model_name, endpoint_name):
        """Deploy model to Azure ML managed endpoint"""
        try:
            # Create endpoint
            endpoint = ManagedOnlineEndpoint(
                name=endpoint_name,
                description="Healthcare Assistant ML endpoint",
                auth_mode="key"
            )
            
            self.ml_client.online_endpoints.begin_create_or_update(endpoint)
            print(f"Endpoint {endpoint_name} created")
            
            # Create deployment
            deployment = ManagedOnlineDeployment(
                name="healthcare-deployment",
                endpoint_name=endpoint_name,
                model=model_name,
                environment="healthcare-env",
                code_path=".",
                scoring_script="score.py",
                instance_type="Standard_DS2_v2",
                instance_count=1
            )
            
            self.ml_client.online_deployments.begin_create_or_update(deployment)
            print(f"Deployment created for {endpoint_name}")
            
        except Exception as e:
            print(f"Error deploying model: {e}")
    
    def test_endpoint(self, endpoint_name, test_data):
        """Test the deployed endpoint"""
        try:
            response = self.ml_client.online_endpoints.invoke(
                endpoint_name=endpoint_name,
                request_file=test_data
            )
            print("Endpoint test successful")
            print(f"Response: {response}")
            return response
        except Exception as e:
            print(f"Error testing endpoint: {e}")
            return None

def main():
    """Main deployment function"""
    # Azure configuration
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_group = os.getenv("AZURE_RESOURCE_GROUP", "healthcare-assistant-rg")
    workspace_name = os.getenv("AZURE_WORKSPACE_NAME", "healthcare-ml-workspace")
    
    if not subscription_id:
        print("Please set AZURE_SUBSCRIPTION_ID environment variable")
        return
    
    # Initialize deployment
    deployment = AzureMLDeployment(subscription_id, resource_group, workspace_name)
    
    # Create environment files
    deployment.create_conda_file()
    deployment.create_scoring_script()
    
    # Create environment
    deployment.create_environment()
    
    # Register models
    models = {}
    for disease in ['diabetes', 'heart_disease', 'eye_disease']:
        model_path = f"models/{disease}_model.pkl"
        if os.path.exists(model_path):
            model = deployment.register_model(model_path, f"healthcare-{disease}-model")
            if model:
                models[disease] = model
    
    # Deploy each model
    for disease, model in models.items():
        endpoint_name = f"healthcare-{disease}-endpoint"
        deployment.deploy_model(model.name, endpoint_name)
    
    print("Deployment completed successfully!")

if __name__ == "__main__":
    main()
