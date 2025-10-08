#!/usr/bin/env python3
"""
Azure Deployment Script for Healthcare Assistant
This script automates the deployment of the Healthcare Assistant to Azure App Service
"""

import os
import json
import subprocess
import sys
from pathlib import Path

class AzureDeployer:
    def __init__(self, resource_group="healthcare-assistant-rg", 
                 app_name="healthcare-assistant-app",
                 location="East US"):
        self.resource_group = resource_group
        self.app_name = app_name
        self.location = location
        self.subscription_id = None
        
    def check_azure_cli(self):
        """Check if Azure CLI is installed and user is logged in"""
        try:
            result = subprocess.run(['az', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Azure CLI is installed")
                return True
            else:
                print("❌ Azure CLI not found. Please install it first.")
                return False
        except FileNotFoundError:
            print("❌ Azure CLI not found. Please install it first.")
            return False
    
    def login_to_azure(self):
        """Login to Azure"""
        print("🔐 Logging into Azure...")
        result = subprocess.run(['az', 'login'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Successfully logged into Azure")
            return True
        else:
            print("❌ Failed to login to Azure")
            print(result.stderr)
            return False
    
    def get_subscription_id(self):
        """Get current subscription ID"""
        result = subprocess.run(['az', 'account', 'show', '--query', 'id', '-o', 'tsv'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            self.subscription_id = result.stdout.strip()
            print(f"✅ Using subscription: {self.subscription_id}")
            return True
        else:
            print("❌ Failed to get subscription ID")
            return False
    
    def create_resource_group(self):
        """Create Azure resource group"""
        print(f"📦 Creating resource group: {self.resource_group}")
        result = subprocess.run([
            'az', 'group', 'create',
            '--name', self.resource_group,
            '--location', self.location
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Resource group created successfully")
            return True
        else:
            print("❌ Failed to create resource group")
            print(result.stderr)
            return False
    
    def create_app_service_plan(self):
        """Create Azure App Service plan"""
        plan_name = f"{self.app_name}-plan"
        print(f"📋 Creating App Service plan: {plan_name}")
        
        result = subprocess.run([
            'az', 'appservice', 'plan', 'create',
            '--name', plan_name,
            '--resource-group', self.resource_group,
            '--location', self.location,
            '--sku', 'B1',  # Basic tier
            '--is-linux'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ App Service plan created successfully")
            return True
        else:
            print("❌ Failed to create App Service plan")
            print(result.stderr)
            return False
    
    def create_web_app(self):
        """Create Azure Web App"""
        plan_name = f"{self.app_name}-plan"
        print(f"🌐 Creating Web App: {self.app_name}")
        
        result = subprocess.run([
            'az', 'webapp', 'create',
            '--name', self.app_name,
            '--resource-group', self.resource_group,
            '--plan', plan_name,
            '--runtime', 'PYTHON|3.11'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Web App created successfully")
            return True
        else:
            print("❌ Failed to create Web App")
            print(result.stderr)
            return False
    
    def configure_app_settings(self):
        """Configure app settings"""
        print("⚙️ Configuring app settings...")
        
        settings = [
            'WEBSITES_ENABLE_APP_SERVICE_STORAGE=false',
            'WEBSITES_PORT=8501',
            'WEBSITES_CONTAINER_START_TIME_LIMIT=1800'
        ]
        
        for setting in settings:
            result = subprocess.run([
                'az', 'webapp', 'config', 'appsettings', 'set',
                '--name', self.app_name,
                '--resource-group', self.resource_group,
                '--settings', setting
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️ Warning: Failed to set {setting}")
        
        print("✅ App settings configured")
        return True
    
    def create_deployment_package(self):
        """Create deployment package"""
        print("📦 Creating deployment package...")
        
        # Create .deployment file
        with open('.deployment', 'w') as f:
            f.write('[config]\n')
            f.write('SCM_DO_BUILD_DURING_DEPLOYMENT=true\n')
        
        # Create web.config for Python
        web_config = '''<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="D:\home\Python311\python.exe"
                  arguments="D:\home\site\wwwroot\streamlit_app.py"
                  stdoutLogEnabled="true"
                  stdoutLogFile="D:\home\LogFiles\python.log"
                  startupTimeLimit="60"
                  startupRetryCount="3">
    </httpPlatform>
  </system.webServer>
</configuration>'''
        
        with open('web.config', 'w') as f:
            f.write(web_config)
        
        print("✅ Deployment package created")
        return True
    
    def deploy_application(self):
        """Deploy the application"""
        print("🚀 Deploying application...")
        
        # Create zip file
        import zipfile
        with zipfile.ZipFile('healthcare-app.zip', 'w') as zipf:
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if not file.endswith(('.zip', '.pyc', '__pycache__')):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
        
        # Deploy using Azure CLI
        result = subprocess.run([
            'az', 'webapp', 'deployment', 'source', 'config-zip',
            '--name', self.app_name,
            '--resource-group', self.resource_group,
            '--src', 'healthcare-app.zip'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Application deployed successfully")
            return True
        else:
            print("❌ Failed to deploy application")
            print(result.stderr)
            return False
    
    def get_app_url(self):
        """Get the deployed app URL"""
        result = subprocess.run([
            'az', 'webapp', 'show',
            '--name', self.app_name,
            '--resource-group', self.resource_group,
            '--query', 'defaultHostName',
            '--output', 'tsv'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            url = f"https://{result.stdout.strip()}"
            print(f"🌐 Your app is available at: {url}")
            return url
        else:
            print("❌ Failed to get app URL")
            return None
    
    def deploy(self):
        """Main deployment method"""
        print("🏥 Starting Azure deployment for Healthcare Assistant...")
        print("=" * 60)
        
        # Check prerequisites
        if not self.check_azure_cli():
            return False
        
        if not self.login_to_azure():
            return False
        
        if not self.get_subscription_id():
            return False
        
        # Deploy resources
        if not self.create_resource_group():
            return False
        
        if not self.create_app_service_plan():
            return False
        
        if not self.create_web_app():
            return False
        
        if not self.configure_app_settings():
            return False
        
        if not self.create_deployment_package():
            return False
        
        if not self.deploy_application():
            return False
        
        # Get app URL
        url = self.get_app_url()
        
        print("=" * 60)
        print("🎉 Deployment completed successfully!")
        if url:
            print(f"🌐 Access your Healthcare Assistant at: {url}")
        print("=" * 60)
        
        return True

def main():
    deployer = AzureDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main()
