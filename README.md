# AI-Powered Healthcare Assistant

A machine learning system that predicts the risk of three common conditions — diabetes, heart disease, and eye disease — based on clinical and lifestyle inputs. The project combines a Flask REST API with a Streamlit dashboard, trained on the UCI Heart Disease Dataset and deployed on Azure.

This started as a portfolio project but ended up being more involved than expected. Getting three separate models to perform well, wiring them into a clean API, and making the dashboard actually usable took considerably more iteration than the final version suggests.

## What it does

A user enters their health metrics — age, BMI, blood pressure, cholesterol, lifestyle factors, family history — and the system returns a risk score and confidence level for each of the three conditions. The interface is designed to be readable by someone without a clinical background, not just a data scientist.

The predictions run locally by default, so no personal health data leaves the machine.

## Models and performance

Three separate models were trained and evaluated. XGBoost won on heart disease by a significant margin; logistic regression generalised better on the other two.

| Condition | Model | AUC Score |
|-----------|-------|-----------|
| Diabetes | Logistic Regression | 0.9729 |
| Heart Disease | XGBoost | 0.9993 |
| Eye Disease | Logistic Regression | 0.9862 |

The heart disease dataset was augmented from 303 to 5,302 samples using feature estimation based on known clinical distributions. SMOTE was applied to handle class imbalance across all three conditions.

## Dataset

The base dataset is the UCI Heart Disease Dataset (Cleveland Clinic Foundation), which contains 303 patient records with 13 clinical features. It is publicly available from the UCI ML Repository.

Features used include age, sex, chest pain type, resting blood pressure, serum cholesterol, fasting blood sugar, resting ECG results, maximum heart rate, exercise-induced angina, ST depression, slope of peak exercise ST segment, number of major vessels coloured by fluoroscopy, and thalassemia type.

Additional lifestyle and demographic features (BMI, smoking, alcohol, exercise frequency, diet quality, family history) were incorporated for the extended diabetes and eye disease models.

## Architecture

The application has two entry points that can run independently or together.

The Flask API handles predictions programmatically. Each disease has its own endpoint, and there is a combined endpoint that returns all three risk scores in a single call.

The Streamlit dashboard provides an interactive interface. Inputs are entered through form controls, predictions update in real time, and the results include confidence intervals and a plain-English risk summary.

```
app.py                  Flask API (port 5000)
streamlit_app.py        Streamlit dashboard (port 8501)
run_app.py              Launches both simultaneously
ml_models.py            Model definitions and training logic
data_preprocessing.py   Cleaning, scaling, encoding
train_models.py         Training script, saves models to /models
```

## Running locally

Clone the repo and set up a virtual environment.

```bash
git clone https://github.com/adilh333/AI-Powered-Healthcare-Assistant.git
cd AI-Powered-Healthcare-Assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Train the models (this takes a few minutes on first run).

```bash
python train_models.py
```

Start the application.

```bash
python run_app.py
```

The dashboard will be available at http://localhost:8501 and the API at http://localhost:5000.

## API reference

All prediction endpoints accept POST requests with a JSON body. The fields are documented in the request schema below. Not all fields are required for every disease type — the preprocessing pipeline handles missing values with median imputation.

```
POST /predict/diabetes
POST /predict/heart_disease
POST /predict/eye_disease
POST /predict/all
```

Example request body:

```json
{
  "age": 52,
  "gender": "Male",
  "bmi": 27.4,
  "systolic_bp": 135,
  "diastolic_bp": 85,
  "cholesterol": 220,
  "glucose": 108,
  "smoking": 1,
  "exercise_frequency": 1,
  "family_heart_disease": 1
}
```

Example response:

```json
{
  "heart_disease": {
    "risk_score": 0.71,
    "risk_level": "High",
    "confidence": 0.94
  }
}
```

Health check and model status are available at GET /health and GET /models/info respectively.

## Deployment

The application is configured for Azure App Service. The deployment scripts handle resource group creation, app service plan setup, and zip deployment.

```bash
python azure_deploy.py
```

Approximate cost on Azure Basic tier is around 13 USD per month. The application can also be deployed to AWS Elastic Beanstalk or any platform that supports Python WSGI apps with minor configuration changes.

## Tech stack

Python 3.8+, Flask, Streamlit, scikit-learn, XGBoost, imbalanced-learn, pandas, NumPy, Plotly, Azure App Service, GitHub Actions for CI/CD.

## Limitations worth noting

The heart disease model's near-perfect AUC on the held-out test set is partly a function of the dataset size and augmentation approach, and should be interpreted cautiously in any real clinical context. These models are not validated for clinical use and are intended as a demonstration of the end-to-end ML pipeline rather than a production medical tool.

The UCI dataset is also relatively small and demographically limited, which affects generalisability. Future work would involve validation on a more diverse dataset and proper clinical evaluation.

## License

MIT
