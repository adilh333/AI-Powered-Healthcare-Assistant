@echo off
REM Azure Deployment Script for Healthcare Assistant
REM This batch file automates the deployment process

echo ============================================================
echo 🏥 Healthcare Assistant - Azure Deployment
echo ============================================================

REM Check if Azure CLI is installed
az --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Azure CLI not found. Please install it first.
    echo Download from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
    pause
    exit /b 1
)

echo ✅ Azure CLI found

REM Login to Azure
echo 🔐 Logging into Azure...
az login
if %errorlevel% neq 0 (
    echo ❌ Failed to login to Azure
    pause
    exit /b 1
)

echo ✅ Successfully logged into Azure

REM Set variables
set RESOURCE_GROUP=healthcare-assistant-rg
set APP_NAME=healthcare-assistant-app
set LOCATION=eastus

echo 📦 Creating resource group: %RESOURCE_GROUP%
az group create --name %RESOURCE_GROUP% --location %LOCATION%
if %errorlevel% neq 0 (
    echo ❌ Failed to create resource group
    pause
    exit /b 1
)

echo ✅ Resource group created

echo 📋 Creating App Service plan...
az appservice plan create --name %APP_NAME%-plan --resource-group %RESOURCE_GROUP% --location %LOCATION% --sku B1 --is-linux
if %errorlevel% neq 0 (
    echo ❌ Failed to create App Service plan
    pause
    exit /b 1
)

echo ✅ App Service plan created

echo 🌐 Creating Web App...
az webapp create --name %APP_NAME% --resource-group %RESOURCE_GROUP% --plan %APP_NAME%-plan --runtime "PYTHON|3.11"
if %errorlevel% neq 0 (
    echo ❌ Failed to create Web App
    pause
    exit /b 1
)

echo ✅ Web App created

echo ⚙️ Configuring app settings...
az webapp config appsettings set --name %APP_NAME% --resource-group %RESOURCE_GROUP% --settings WEBSITES_ENABLE_APP_SERVICE_STORAGE=false
az webapp config appsettings set --name %APP_NAME% --resource-group %RESOURCE_GROUP% --settings WEBSITES_PORT=8501
az webapp config appsettings set --name %APP_NAME% --resource-group %RESOURCE_GROUP% --settings WEBSITES_CONTAINER_START_TIME_LIMIT=1800

echo ✅ App settings configured

echo 📦 Creating deployment package...
python azure_deploy.py
if %errorlevel% neq 0 (
    echo ❌ Failed to create deployment package
    pause
    exit /b 1
)

echo ✅ Deployment package created

echo 🚀 Deploying application...
az webapp deployment source config-zip --name %APP_NAME% --resource-group %RESOURCE_GROUP% --src healthcare-app.zip
if %errorlevel% neq 0 (
    echo ❌ Failed to deploy application
    pause
    exit /b 1
)

echo ✅ Application deployed successfully

echo 🌐 Getting app URL...
az webapp show --name %APP_NAME% --resource-group %RESOURCE_GROUP% --query defaultHostName --output tsv > app_url.txt
set /p APP_URL=<app_url.txt
echo.
echo ============================================================
echo 🎉 Deployment completed successfully!
echo 🌐 Your Healthcare Assistant is available at:
echo    https://%APP_URL%
echo ============================================================
echo.
echo 📋 Next steps:
echo 1. Wait 5-10 minutes for the app to fully start
echo 2. Visit the URL above to access your application
echo 3. Check the Azure portal for monitoring and logs
echo.

del app_url.txt
pause
