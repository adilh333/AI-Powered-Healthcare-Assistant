#!/usr/bin/env python3
"""
GitHub Repository Setup Script for Healthcare Assistant
This script helps set up the project for GitHub with proper structure and files
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_git_status():
    """Check if git is initialized and configured"""
    print("🔍 Checking Git status...")
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("📁 Initializing Git repository...")
        if not run_command("git init", "Git initialization"):
            return False
    
    # Check git config
    result = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("⚠️  Git user.name not configured. Please run:")
        print("   git config --global user.name 'Your Name'")
        print("   git config --global user.email 'your.email@example.com'")
        return False
    
    return True

def create_github_structure():
    """Create GitHub-specific files and structure"""
    print("📁 Creating GitHub project structure...")
    
    # Create directories
    directories = [
        'tests',
        '.github/workflows',
        'docs',
        'scripts',
        'examples'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def update_gitignore():
    """Update .gitignore with comprehensive rules"""
    print("📝 Updating .gitignore...")
    
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Project specific
models/
data/
*.zip
*.tar.gz
*.rar

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Azure
.azure/
azure-deployment-guide.md

# Logs
*.log
logs/

# Temporary files
temp/
tmp/
*.tmp

# Model files (too large for GitHub)
*.pkl
*.joblib
*.h5
*.hdf5

# Data files
*.csv
*.json
*.xlsx
*.parquet

# Streamlit
.streamlit/

# Jupyter
*.ipynb

# Documentation builds
docs/build/
site/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Updated .gitignore")
    return True

def create_github_workflows():
    """Create GitHub Actions workflows"""
    print("🔧 Creating GitHub Actions workflows...")
    
    # CI/CD workflow
    ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check code formatting with black
      run: |
        black --check --diff .
    
    - name: Check import sorting with isort
      run: |
        isort --check-only --diff .
    
    - name: Type check with mypy
      run: |
        mypy . --ignore-missing-imports
    
    - name: Security check with bandit
      run: |
        bandit -r . -f json -o bandit-report.json || true
    
    - name: Test with pytest
      run: |
        pytest --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package
      run: |
        twine check dist/*
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/
"""
    
    with open('.github/workflows/ci.yml', 'w') as f:
        f.write(ci_workflow)
    
    print("✅ Created CI/CD workflow")
    return True

def create_documentation():
    """Create additional documentation files"""
    print("📚 Creating documentation files...")
    
    # Create docs directory structure
    docs_files = {
        'docs/installation.md': """# Installation Guide

## Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- Git (for cloning)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/Healthcare_Assistant.git
cd Healthcare_Assistant
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Or using conda
conda create -n healthcare-assistant python=3.11
conda activate healthcare-assistant
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models
```bash
python train_models.py
```

### 5. Start Application
```bash
python run_app.py
```

## Troubleshooting

### Common Issues
1. **Port already in use**: Change ports in configuration
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Model loading errors**: Ensure models are trained first
""",
        
        'docs/api-reference.md': """# API Reference

## Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Check application health

### Model Information
- **URL**: `/models/info`
- **Method**: GET
- **Description**: Get information about loaded models

### Disease Predictions
- **URL**: `/predict/{disease_type}`
- **Method**: POST
- **Description**: Predict disease risk
- **Disease Types**: diabetes, heart_disease, eye_disease

### All Predictions
- **URL**: `/predict/all`
- **Method**: POST
- **Description**: Get predictions for all diseases

## Request/Response Examples

See main README.md for detailed examples.
""",
        
        'docs/deployment.md': """# Deployment Guide

## Local Deployment
1. Follow installation guide
2. Run `python run_app.py`
3. Access at http://localhost:8501

## Azure Deployment
1. Install Azure CLI
2. Run `deploy-to-azure.bat`
3. Access deployed app at Azure URL

## Docker Deployment
```bash
docker build -t healthcare-assistant .
docker run -p 8501:8501 healthcare-assistant
```

## Production Considerations
- Use production WSGI server (Gunicorn)
- Configure proper logging
- Set up monitoring and alerts
- Use environment variables for configuration
"""
    }
    
    for file_path, content in docs_files.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created {file_path}")
    
    return True

def create_examples():
    """Create example files"""
    print("📝 Creating example files...")
    
    examples = {
        'examples/basic_usage.py': """#!/usr/bin/env python3
\"\"\"
Basic usage example for Healthcare Assistant API
\"\"\"

import requests
import json

# API base URL
API_URL = "http://localhost:5000"

def test_health():
    \"\"\"Test health endpoint\"\"\"
    response = requests.get(f"{API_URL}/health")
    print("Health Status:", response.json())

def test_prediction():
    \"\"\"Test disease prediction\"\"\"
    # Sample patient data
    patient_data = {
        "age": 45,
        "gender": "Male",
        "bmi": 25.5,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "heart_rate": 70,
        "glucose": 100,
        "cholesterol": 200,
        "hdl_cholesterol": 50,
        "ldl_cholesterol": 120,
        "triglycerides": 150,
        "smoking": 0,
        "alcohol_consumption": 1,
        "exercise_frequency": 2,
        "diet_quality": 3,
        "family_diabetes": 0,
        "family_heart_disease": 0,
        "family_eye_disease": 0,
        "hypertension": 0,
        "previous_stroke": 0,
        "kidney_disease": 0
    }
    
    # Get predictions
    response = requests.post(
        f"{API_URL}/predict/all",
        json=patient_data
    )
    
    if response.status_code == 200:
        predictions = response.json()
        print("Disease Risk Predictions:")
        for disease, risk in predictions.items():
            print(f"  {disease}: {risk['risk_level']} ({risk['risk_score']:.2f})")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    print("Testing Healthcare Assistant API...")
    test_health()
    test_prediction()
""",
        
        'examples/advanced_usage.py': """#!/usr/bin/env python3
\"\"\"
Advanced usage example for Healthcare Assistant
\"\"\"

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class HealthcareClient:
    def __init__(self, api_url="http://localhost:5000"):
        self.api_url = api_url
    
    def get_health_status(self):
        \"\"\"Get API health status\"\"\"
        response = requests.get(f"{self.api_url}/health")
        return response.json()
    
    def get_model_info(self):
        \"\"\"Get model information\"\"\"
        response = requests.get(f"{self.api_url}/models/info")
        return response.json()
    
    def predict_disease(self, patient_data, disease_type="all"):
        \"\"\"Predict disease risk\"\"\"
        endpoint = f"/predict/{disease_type}" if disease_type != "all" else "/predict/all"
        response = requests.post(f"{self.api_url}{endpoint}", json=patient_data)
        return response.json()
    
    def batch_predict(self, patients_df):
        \"\"\"Predict for multiple patients\"\"\"
        results = []
        for _, patient in patients_df.iterrows():
            prediction = self.predict_disease(patient.to_dict())
            results.append(prediction)
        return results

def create_sample_data():
    \"\"\"Create sample patient data\"\"\"
    return pd.DataFrame({
        'age': [45, 50, 35, 60, 40],
        'gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'bmi': [25.5, 28.2, 22.1, 30.5, 26.8],
        'systolic_bp': [120, 140, 110, 160, 130],
        'diastolic_bp': [80, 90, 70, 100, 85],
        'heart_rate': [70, 85, 65, 95, 75],
        'glucose': [100, 120, 90, 150, 110],
        'cholesterol': [200, 250, 180, 300, 220],
        'hdl_cholesterol': [50, 45, 55, 40, 48],
        'ldl_cholesterol': [120, 150, 100, 200, 130],
        'triglycerides': [150, 200, 120, 250, 170],
        'smoking': [0, 1, 0, 1, 0],
        'alcohol_consumption': [1, 2, 0, 3, 1],
        'exercise_frequency': [2, 1, 3, 0, 2],
        'diet_quality': [3, 2, 4, 1, 3],
        'family_diabetes': [0, 1, 0, 1, 0],
        'family_heart_disease': [0, 0, 1, 1, 0],
        'family_eye_disease': [0, 0, 1, 0, 0],
        'hypertension': [0, 1, 0, 1, 0],
        'previous_stroke': [0, 0, 0, 1, 0],
        'kidney_disease': [0, 0, 0, 0, 0]
    })

def visualize_predictions(results):
    \"\"\"Visualize prediction results\"\"\"
    diseases = ['diabetes', 'heart_disease', 'eye_disease']
    risk_scores = {disease: [] for disease in diseases}
    
    for result in results:
        for disease in diseases:
            risk_scores[disease].append(result[disease]['risk_score'])
    
    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    for i, disease in enumerate(diseases):
        axes[i].hist(risk_scores[disease], bins=10, alpha=0.7)
        axes[i].set_title(f'{disease.replace("_", " ").title()} Risk Distribution')
        axes[i].set_xlabel('Risk Score')
        axes[i].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Initialize client
    client = HealthcareClient()
    
    # Check health
    print("API Health:", client.get_health_status())
    
    # Get model info
    print("Model Info:", client.get_model_info())
    
    # Create sample data
    patients = create_sample_data()
    print(f"Created {len(patients)} sample patients")
    
    # Get predictions
    results = client.batch_predict(patients)
    
    # Display results
    for i, result in enumerate(results):
        print(f"\\nPatient {i+1} Predictions:")
        for disease, risk in result.items():
            print(f"  {disease}: {risk['risk_level']} ({risk['risk_score']:.2f})")
    
    # Visualize results
    visualize_predictions(results)
"""
    }
    
    for file_path, content in examples.items():
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created {file_path}")
    
    return True

def setup_git_repository():
    """Set up Git repository with initial commit"""
    print("🔧 Setting up Git repository...")
    
    commands = [
        ("git add .", "Adding files to Git"),
        ("git commit -m 'Initial commit: Healthcare Assistant project setup'", "Creating initial commit"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def print_next_steps():
    """Print next steps for GitHub setup"""
    print("\n" + "="*60)
    print("🎉 GitHub Repository Setup Complete!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Create a new repository on GitHub")
    print("2. Add your repository as remote origin:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/Healthcare_Assistant.git")
    print("3. Push your code to GitHub:")
    print("   git push -u origin main")
    print("4. Update the repository URL in README.md")
    print("5. Enable GitHub Actions in repository settings")
    print("6. Set up branch protection rules")
    print("7. Add collaborators if needed")
    print("\n🔗 Useful GitHub Features to Enable:")
    print("- Issues and Discussions")
    print("- Wiki (for additional documentation)")
    print("- Projects (for project management)")
    print("- Security alerts")
    print("- Dependabot (for dependency updates)")
    print("\n📚 Documentation:")
    print("- README.md: Main project documentation")
    print("- CONTRIBUTING.md: Contribution guidelines")
    print("- LICENSE: MIT License")
    print("- docs/: Additional documentation")
    print("- examples/: Usage examples")
    print("\n🧪 Testing:")
    print("- Run tests: pytest")
    print("- Code quality: black, flake8, mypy")
    print("- Security: bandit")
    print("\n🚀 Deployment:")
    print("- Azure: deploy-to-azure.bat")
    print("- Docker: docker build -t healthcare-assistant .")
    print("- Local: python run_app.py")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("🏥 Healthcare Assistant - GitHub Repository Setup")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: Please run this script from the Healthcare_Assistant directory")
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Checking Git status", check_git_status),
        ("Creating GitHub structure", create_github_structure),
        ("Updating .gitignore", update_gitignore),
        ("Creating GitHub workflows", create_github_workflows),
        ("Creating documentation", create_documentation),
        ("Creating examples", create_examples),
        ("Setting up Git repository", setup_git_repository),
    ]
    
    for step_name, step_function in steps:
        print(f"\n🔄 {step_name}...")
        if not step_function():
            print(f"❌ {step_name} failed!")
            sys.exit(1)
        print(f"✅ {step_name} completed!")
    
    print_next_steps()

if __name__ == "__main__":
    main()
