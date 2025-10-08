#!/bin/bash

# Healthcare Assistant Deployment Script
echo "Starting Healthcare Assistant deployment..."

# Set environment variables
export AZURE_SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID:-""}
export AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP:-"healthcare-assistant-rg"}
export AZURE_WORKSPACE_NAME=${AZURE_WORKSPACE_NAME:-"healthcare-ml-workspace"}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI is not installed. Please install it first."
    exit 1
fi

# Login to Azure (if not already logged in)
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "Please login to Azure CLI:"
    az login
fi

# Create resource group if it doesn't exist
echo "Creating resource group..."
az group create --name $AZURE_RESOURCE_GROUP --location "East US"

# Create Azure ML workspace
echo "Creating Azure ML workspace..."
az ml workspace create --name $AZURE_WORKSPACE_NAME --resource-group $AZURE_RESOURCE_GROUP

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Train and save models
echo "Training ML models..."
python -c "
from ml_models import HealthcareMLPipeline
pipeline = HealthcareMLPipeline()
pipeline.train_all_models(n_samples=10000)
print('Models trained and saved successfully')
"

# Deploy to Azure ML
echo "Deploying to Azure ML..."
python azure_deployment.py

# Deploy Azure Functions
echo "Deploying Azure Functions..."
cd azure_functions
func azure functionapp publish healthcare-assistant-functions --python
cd ..

# Deploy Streamlit to Azure App Service
echo "Deploying Streamlit dashboard to Azure App Service..."
az webapp create --resource-group $AZURE_RESOURCE_GROUP --plan healthcare-app-plan --name healthcare-assistant-app --runtime "PYTHON|3.9"

# Configure app settings
az webapp config appsettings set --resource-group $AZURE_RESOURCE_GROUP --name healthcare-assistant-app --settings @azure_app_settings.json

# Deploy code
az webapp deployment source config-zip --resource-group $AZURE_RESOURCE_GROUP --name healthcare-assistant-app --src healthcare-app.zip

echo "Deployment completed successfully!"
echo "Your Healthcare Assistant is now deployed on Azure."
