# AI-Powered Healthcare Assistant

A machine learning system that predicts the risk of three common conditions — diabetes, heart disease, and eye disease — based on clinical and lifestyle inputs. Built with a Streamlit dashboard and deployed on Streamlit Community Cloud.

**Live demo:** https://ai-powered-healthcare-assistant-3syvu4kon33nzxappni4z2x.streamlit.app

This started as a portfolio project but ended up being more involved than expected. Getting three separate models to perform well, handling class imbalance across all three conditions, and making the dashboard actually usable took considerably more iteration than the final version suggests.

## What it does

A user enters their health metrics — age, BMI, blood pressure, cholesterol, lifestyle factors, family history — and the system returns a risk score and confidence level for each of the three conditions. The interface is designed to be readable by someone without a clinical background, not just a data scientist.

All predictions run locally within the Streamlit environment. No personal health data is stored or transmitted.

## Models and performance

Three separate models were trained and evaluated. XGBoost won on heart disease by a significant margin; logistic regression generalised better on the other two.

| Condition | Model | AUC Score |
|-----------|-------|-----------|
| Diabetes | Logistic Regression | 0.9805 |
| Heart Disease | XGBoost | 0.9992 |
| Eye Disease | Logistic Regression | 0.9864 |

SMOTE was applied to handle class imbalance across all three conditions.

## Dataset

The base dataset is the UCI Heart Disease Dataset (Cleveland Clinic Foundation), which contains 303 patient records with 13 clinical features. It is publicly available from the UCI ML Repository.

Features used include age, sex, chest pain type, resting blood pressure, serum cholesterol, fasting blood sugar, resting ECG results, maximum heart rate, exercise-induced angina, ST depression, slope of peak exercise ST segment, number of major vessels coloured by fluoroscopy, and thalassemia type.

Additional lifestyle and demographic features (BMI, smoking, alcohol, exercise frequency, diet quality, family history) were incorporated for the extended diabetes and eye disease models.

## Project structure

```
AI-Powered-Healthcare-Assistant/
├── streamlit_app.py          Main Streamlit dashboard
├── ml_models.py              Model definitions and prediction logic
├── data_preprocessing.py     Cleaning, scaling, encoding pipeline
├── train_models.py           Training script, saves models to /models
├── models/                   Trained model and scaler files (.pkl)
│   ├── diabetes_model.pkl
│   ├── diabetes_scaler.pkl
│   ├── heart_disease_model.pkl
│   ├── heart_disease_scaler.pkl
│   ├── eye_disease_model.pkl
│   ├── eye_disease_scaler.pkl
│   └── feature_columns.pkl
├── requirements.txt          Python dependencies
└── README.md
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

Train the models (this takes a few minutes on first run and saves the .pkl files to the models folder).

```bash
python train_models.py
```

Start the dashboard.

```bash
streamlit run streamlit_app.py
```

The dashboard will be available at http://localhost:8501.

## Tech stack

Python 3.8+, Streamlit, scikit-learn, XGBoost, imbalanced-learn, pandas, NumPy, Plotly, streamlit-option-menu.

## Limitations worth noting

The heart disease model's near-perfect AUC on the held-out test set is partly a function of the dataset size and augmentation approach, and should be interpreted cautiously in any real clinical context. These models are not validated for clinical use and are intended as a demonstration of the end-to-end ML pipeline rather than a production medical tool.

The UCI dataset is also relatively small and demographically limited, which affects generalisability. Future work would involve validation on a more diverse dataset and proper clinical evaluation.

## License

MIT
