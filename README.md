# 🏥 AI-Powered Healthcare Assistant

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Build Status](https://github.com/YOUR_USERNAME/Healthcare_Assistant/workflows/CI/badge.svg)](https://github.com/YOUR_USERNAME/Healthcare_Assistant/actions)

An intelligent healthcare prediction system that uses machine learning to predict disease risks and provide personalized health recommendations. Built with real-world UCI Heart Disease Dataset and deployed on Azure cloud.

## 🌟 Features

- **🎯 Disease Risk Prediction**: Predict diabetes, heart disease, and eye disease risks
- **⚡ Real-time Analysis**: Get instant predictions with detailed risk scores
- **📊 Interactive Dashboard**: User-friendly Streamlit interface with visualizations
- **🔌 REST API**: Programmatic access via Flask API with comprehensive endpoints
- **☁️ Cloud Ready**: Deploy to Azure, AWS, or any cloud platform
- **📈 UCI Dataset Integration**: Trained on real-world UCI Heart Disease Dataset
- **🔒 Privacy Focused**: Local processing, no personal data storage
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

## 🚀 Tech Stack

### Backend & API
- **Python 3.8+** - Core programming language
- **Flask** - REST API server with CORS support
- **Streamlit** - Interactive dashboard framework
- **Gunicorn** - Production WSGI server

### Machine Learning
- **scikit-learn** - Core ML algorithms and preprocessing
- **XGBoost** - Gradient boosting for high accuracy
- **pandas & numpy** - Data manipulation and numerical computing
- **imbalanced-learn** - SMOTE for handling class imbalance
- **joblib** - Model serialization and persistence

### Frontend & Visualization
- **Streamlit** - Interactive web application
- **Plotly** - Interactive charts and graphs
- **Altar** - Statistical visualizations
- **Matplotlib & Seaborn** - Static plots and statistical graphics

### Cloud & Deployment
- **Azure App Service** - Web application hosting
- **Azure ML** - Model management and deployment
- **Azure Functions** - Serverless computing
- **Azure Storage** - Data and model storage
- **GitHub Actions** - CI/CD pipeline

## 📊 Dataset & Model Performance

### UCI Heart Disease Dataset
- **Source**: [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/heart+disease)
- **Original Size**: 303 samples
- **Extended Size**: 5,302 samples (for better training)
- **Features**: 13 clinical + 8 estimated features
- **Target**: Binary classification (disease/no disease)

### Model Performance (AUC Scores)

| Disease Type | Best Model | AUC Score | Features Used |
|--------------|------------|-----------|---------------|
| **Diabetes** | Logistic Regression | **0.9729** | 18 clinical & lifestyle factors |
| **Heart Disease** | XGBoost | **0.9993** | 21 clinical & lifestyle factors |
| **Eye Disease** | Logistic Regression | **0.9862** | 19 clinical & lifestyle factors |

### Key Features
- **Demographics**: Age, Gender, BMI
- **Vital Signs**: Blood pressure, heart rate
- **Lab Values**: Cholesterol, glucose, triglycerides
- **Lifestyle**: Smoking, alcohol, exercise, diet quality
- **Family History**: Diabetes, heart disease, eye disease
- **Medical History**: Hypertension, stroke, kidney disease
- **Heart-Specific**: Chest pain type, exercise angina, ST depression, major vessels, thalassemia

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- Git (for cloning)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/Healthcare_Assistant.git
cd Healthcare_Assistant
```

2. **Create virtual environment**
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n healthcare-assistant python=3.11
conda activate healthcare-assistant
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Train ML models**
```bash
python train_models.py
```

5. **Start the application**
```bash
# Option 1: Start both API and Dashboard
python run_app.py

# Option 2: Start individually
python app.py                    # Flask API (port 5000)
streamlit run streamlit_app.py  # Streamlit Dashboard (port 8501)
```

### Access Application
- **🖥️ Streamlit Dashboard**: http://localhost:8501
- **🔌 Flask API**: http://localhost:5000
- **📖 API Documentation**: http://localhost:5000/health

## 📖 API Documentation

### Health & Status Endpoints

#### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-02T22:00:00Z",
  "models_loaded": 3
}
```

#### Model Information
```http
GET /models/info
```
**Response:**
```json
{
  "diabetes": {
    "status": "Loaded",
    "accuracy": 0.9729,
    "model_type": "Logistic Regression"
  },
  "heart_disease": {
    "status": "Loaded",
    "accuracy": 0.9993,
    "model_type": "XGBoost"
  },
  "eye_disease": {
    "status": "Loaded", 
    "accuracy": 0.9862,
    "model_type": "Logistic Regression"
  }
}
```

### Prediction Endpoints

#### Individual Disease Predictions
```http
POST /predict/diabetes
POST /predict/heart_disease  
POST /predict/eye_disease
```

#### All Diseases Prediction
```http
POST /predict/all
```

### Request Format
```json
{
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
  "kidney_disease": 0,
  "chest_pain_type": "Typical Angina",
  "exercise_angina": 0,
  "st_depression": 0.0,
  "major_vessels": 0,
  "thalassemia": "Normal"
}
```

### Response Format
```json
{
  "diabetes": {
    "risk_score": 0.23,
    "risk_level": "Low",
    "confidence": 0.95
  },
  "heart_disease": {
    "risk_score": 0.15,
    "risk_level": "Low",
    "confidence": 0.99
  },
  "eye_disease": {
    "risk_score": 0.08,
    "risk_level": "Low",
    "confidence": 0.98
  }
}
```

## 🏗️ Project Structure

```
Healthcare_Assistant/
├── 📁 Core Application
│   ├── app.py                 # Flask API server
│   ├── streamlit_app.py       # Streamlit dashboard
│   ├── run_app.py             # Application launcher
│   └── startup.py             # Azure startup script
├── 🤖 Machine Learning
│   ├── ml_models.py           # ML pipeline and models
│   ├── data_preprocessing.py  # Data preprocessing
│   ├── data_loader.py         # UCI dataset loader
│   └── train_models.py        # Model training script
├── 📊 Data & Models
│   ├── models/                # Trained ML models
│   └── data/                  # Dataset files
├── 🧪 Testing
│   ├── tests/                 # Test files
│   ├── test_api.py            # API testing
│   └── test_uci_integration.py # UCI integration tests
├── ☁️ Deployment
│   ├── azure_deploy.py        # Azure deployment script
│   ├── deploy-to-azure.bat    # Windows deployment
│   ├── requirements-azure.txt # Azure dependencies
│   └── azure-deployment-guide.md
├── 🔧 Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── requirements-dev.txt   # Development dependencies
│   ├── setup.py              # Package setup
│   ├── pyproject.toml        # Modern Python packaging
│   └── .gitignore            # Git ignore rules
├── 📚 Documentation
│   ├── README.md              # This file
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── LICENSE                # MIT License
│   └── .github/workflows/     # CI/CD workflows
└── 🚀 Scripts
    ├── start_healthcare_app.bat # Windows launcher
    └── start_healthcare_app.sh  # Linux/Mac launcher
```

## 🤖 Machine Learning Pipeline

### Data Preprocessing Workflow
1. **📥 Data Loading**: UCI Heart Disease Dataset download and parsing
2. **🧹 Data Cleaning**: Handle missing values and outliers
3. **🔧 Feature Engineering**: Create derived features and interactions
4. **📏 Data Scaling**: StandardScaler normalization for numerical features
5. **🏷️ Encoding**: Label encoding for categorical variables
6. **✂️ Train/Test Split**: 80/20 split with stratification

### Model Training Process
1. **🔄 Multiple Algorithms**: Random Forest, XGBoost, Logistic Regression
2. **📊 Cross-Validation**: 5-fold CV for robust evaluation
3. **⚙️ Hyperparameter Tuning**: Grid search optimization
4. **🏆 Model Selection**: Best performing model per disease type
5. **💾 Model Persistence**: Save trained models and preprocessors

### Model Evaluation Metrics
- **🎯 AUC Score**: Primary metric for binary classification
- **📈 Precision/Recall**: Disease-specific performance analysis
- **📊 Confusion Matrix**: Detailed performance breakdown
- **🔍 Feature Importance**: Model interpretability and insights

## ☁️ Azure Cloud Deployment

### Prerequisites
- Azure account ([Free tier available](https://azure.microsoft.com/free/))
- Azure CLI installed ([Download here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))

### 🚀 Automated Deployment (Recommended)
```bash
# Windows
deploy-to-azure.bat

# Linux/Mac
python azure_deploy.py
```

### 🔧 Manual Deployment Steps

1. **Login to Azure**
```bash
az login
```

2. **Create Resource Group**
```bash
az group create --name healthcare-assistant-rg --location eastus
```

3. **Create App Service Plan**
```bash
az appservice plan create --name healthcare-plan --resource-group healthcare-assistant-rg --sku B1 --is-linux
```

4. **Create Web App**
```bash
az webapp create --name healthcare-app --resource-group healthcare-assistant-rg --plan healthcare-plan --runtime "PYTHON|3.11"
```

5. **Configure App Settings**
```bash
az webapp config appsettings set --name healthcare-app --resource-group healthcare-assistant-rg --settings WEBSITES_PORT=8501
```

6. **Deploy Application**
```bash
az webapp deployment source config-zip --name healthcare-app --resource-group healthcare-assistant-rg --src healthcare-app.zip
```

### 🌐 Access Deployed Application
- **URL**: https://healthcare-app.azurewebsites.net
- **Monitoring**: Azure Portal → App Service → Monitoring
- **Logs**: Azure Portal → App Service → Log stream
- **Cost**: ~$13/month for Basic tier

## 🧪 Testing & Quality Assurance

### Running Tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_ml_models.py -v

# Run integration tests
pytest tests/ -m integration
```

### Test Coverage
- **✅ Unit Tests**: Individual component testing
- **🔗 Integration Tests**: End-to-end workflow testing
- **🌐 API Tests**: Flask endpoint testing
- **🤖 ML Tests**: Model training and prediction testing
- **📊 Data Tests**: Data preprocessing and validation

### Code Quality
```bash
# Code formatting
black .

# Import sorting
isort .

# Linting
flake8 .

# Type checking
mypy .

# Security scanning
bandit -r .
```

## 📈 Performance Optimization

### Model Optimization
- **🎯 Feature Selection**: Remove redundant and low-importance features
- **⚙️ Hyperparameter Tuning**: Optimize model parameters for best performance
- **🔄 Ensemble Methods**: Combine multiple models for improved accuracy
- **📦 Model Compression**: Reduce model size for faster inference

### Application Optimization
- **💾 Caching**: Cache model predictions and preprocessed data
- **⚡ Async Processing**: Non-blocking API calls for better performance
- **🗄️ Database Optimization**: Efficient data storage and retrieval
- **🌐 CDN**: Content delivery network for static assets

## 🔒 Security & Privacy

### Data Privacy
- **🔐 No Personal Data**: Only health metrics, no personal identifiers
- **🏠 Local Processing**: Data stays on your device/cloud instance
- **🔒 Encryption**: Secure data transmission with HTTPS
- **📋 Compliance**: HIPAA considerations for healthcare data

### API Security
- **🚦 Rate Limiting**: Prevent API abuse and ensure fair usage
- **✅ Input Validation**: Sanitize and validate all user inputs
- **🌐 CORS**: Proper cross-origin resource sharing configuration
- **🔐 HTTPS**: Secure connections for all communications

## 🤝 Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Development Setup
```bash
# Fork and clone repository
git clone https://github.com/YOUR_USERNAME/Healthcare_Assistant.git
cd Healthcare_Assistant

# Create feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests to ensure everything works
pytest

# Make your changes and test
# ... your development work ...

# Run code quality checks
black .
isort .
flake8 .
mypy .

# Commit and push
git add .
git commit -m "Add: Your feature description"
git push origin feature/your-feature-name
```

### Contribution Guidelines
- **🐛 Bug Reports**: Use GitHub Issues with detailed reproduction steps
- **💡 Feature Requests**: Open issues with clear descriptions
- **📝 Documentation**: Help improve docs and examples
- **🧪 Testing**: Add tests for new features and bug fixes
- **📊 Performance**: Optimize code and improve efficiency

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **🏥 UCI ML Repository** for the Heart Disease Dataset
- **🤖 scikit-learn** for machine learning algorithms and tools
- **📊 Streamlit** for the interactive dashboard framework
- **☁️ Azure** for cloud deployment platform and services
- **🌍 Open source community** for various libraries and tools
- **👥 Contributors** who help improve this project

## 📞 Support & Community

- **🐛 Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Healthcare_Assistant/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Healthcare_Assistant/discussions)
- **📧 Email**: healthcare.assistant@example.com
- **📖 Documentation**: [Project Wiki](https://github.com/YOUR_USERNAME/Healthcare_Assistant/wiki)

## 🗺️ Roadmap

### Version 1.1 (Q2 2025)
- [ ] 🧠 Add more disease prediction models (cancer, stroke, kidney disease)
- [ ] 🔐 Implement user authentication and session management
- [ ] 📊 Enhanced data visualization and analytics dashboard
- [ ] 📱 Mobile app integration and responsive improvements

### Version 1.2 (Q3 2025)
- [ ] ⏱️ Real-time health monitoring and alerts
- [ ] ⌚ Integration with wearable devices (Fitbit, Apple Watch)
- [ ] 📈 Advanced analytics and trend analysis
- [ ] 🌍 Multi-language support (Spanish, French, German)

### Version 2.0 (Q4 2025)
- [ ] 🧠 Deep learning models (CNN, RNN, Transformer)
- [ ] 🖼️ Medical image analysis (X-rays, MRI, CT scans)
- [ ] 💊 Drug interaction checker and medication recommendations
- [ ] 🏥 Telemedicine integration and doctor consultations

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/Healthcare_Assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/Healthcare_Assistant?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/Healthcare_Assistant)
![GitHub pull requests](https://img.shields.io/github/issues-pr/YOUR_USERNAME/Healthcare_Assistant)

---

**🏥 Built with ❤️ for better healthcare outcomes**

*Empowering healthcare professionals and patients with AI-driven insights for early disease detection and prevention.*