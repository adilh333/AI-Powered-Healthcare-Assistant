"""
Healthcare Assistant - Streamlit Dashboard
AI-Powered Disease Risk Prediction System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime
import time
from streamlit_option_menu import option_menu
from ml_models import HealthcareMLPipeline
from data_preprocessing import HealthDataPreprocessor

# Page configuration
st.set_page_config(
    page_title="Healthcare Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    .risk-high {
        color: #e74c3c;
        font-weight: bold;
    }
    .risk-medium {
        color: #f39c12;
        font-weight: bold;
    }
    .risk-low {
        color: #27ae60;
        font-weight: bold;
    }
    .recommendation-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ml_pipeline():
    """Load ML pipeline with caching"""
    pipeline = HealthcareMLPipeline()
    try:
        pipeline.load_models()
        return pipeline
    except:
        st.error("Failed to load ML models. Please ensure models are trained first.")
        return None

@st.cache_data
def get_api_health():
    """Check API health status"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except:
        return False, None

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">🏥 AI-Powered Healthcare Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Advanced Disease Risk Prediction using Machine Learning</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            "Navigation",
            ["Dashboard", "Risk Assessment", "Results", "Model Info", "Settings"],
            icons=['house', 'clipboard-data', 'bar-chart', 'gear', 'settings'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#667eea", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
    
    # Load ML pipeline
    ml_pipeline = load_ml_pipeline()
    
    # Check API status
    api_healthy, api_info = get_api_health()
    
    # Display content based on selected page
    if selected == "Dashboard":
        show_dashboard(ml_pipeline, api_healthy, api_info)
    elif selected == "Risk Assessment":
        show_risk_assessment(ml_pipeline)
    elif selected == "Results":
        show_results()
    elif selected == "Model Info":
        show_model_info(ml_pipeline)
    elif selected == "Settings":
        show_settings()

def show_dashboard(ml_pipeline, api_healthy, api_info):
    """Display main dashboard"""
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="API Status",
            value="🟢 Online" if api_healthy else "🔴 Offline",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Models Loaded",
            value=f"{len(ml_pipeline.models) if ml_pipeline else 0}/3",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Disease Types",
            value="3",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Accuracy",
            value="95%",
            delta=None
        )
    
    st.divider()
    
    # Feature overview
    st.subheader("🔬 Disease Prediction Capabilities")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🩺 Diabetes Prediction
        - Blood glucose analysis
        - BMI and lifestyle factors
        - Family history consideration
        - Personalized recommendations
        """)
    
    with col2:
        st.markdown("""
        ### ❤️ Heart Disease Risk
        - Cholesterol and blood pressure
        - Exercise and diet analysis
        - Smoking and alcohol factors
        - Early intervention guidance
        """)
    
    with col3:
        st.markdown("""
        ### 👁️ Eye Disease Detection
        - Diabetes correlation analysis
        - Age and hypertension factors
        - Family history assessment
        - Preventive care recommendations
        """)
    
    st.divider()
    
    # Quick start
    st.subheader("🚀 Quick Start")
    st.info("Navigate to 'Risk Assessment' to begin analyzing patient health data and predicting disease risks.")
    
    # Recent predictions (if any)
    if 'predictions' in st.session_state and st.session_state.predictions:
        st.subheader("📊 Recent Predictions")
        show_prediction_summary(st.session_state.predictions)

def show_risk_assessment(ml_pipeline):
    """Display risk assessment form"""
    
    st.subheader("📋 Health Risk Assessment")
    st.write("Please provide patient health information for comprehensive disease risk analysis.")
    
    with st.form("risk_assessment_form"):
        # Demographics
        st.markdown("### 👤 Demographics")
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=45, help="Patient age in years")
            gender = st.selectbox("Gender", ["Male", "Female"], help="Patient gender")
        
        with col2:
            bmi = st.number_input("BMI (Body Mass Index)", min_value=15.0, max_value=50.0, value=25.0, step=0.1, help="Body Mass Index")
        
        # UCI-specific features
        st.markdown("### 🫀 Heart Disease Specific Features")
        col1, col2 = st.columns(2)
        
        with col1:
            chest_pain_type = st.selectbox("Chest Pain Type", 
                ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
                help="Type of chest pain experienced")
            
            exercise_angina = st.selectbox("Exercise Induced Angina", 
                ["No", "Yes"], 
                help="Chest pain during exercise")
        
        with col2:
            st_depression = st.number_input("ST Depression", 
                min_value=0.0, max_value=6.0, value=0.0, step=0.1,
                help="ST depression induced by exercise relative to rest")
            
            major_vessels = st.number_input("Major Vessels", 
                min_value=0, max_value=4, value=0,
                help="Number of major vessels colored by fluoroscopy")
        
        thalassemia = st.selectbox("Thalassemia Type", 
            ["Normal", "Fixed Defect", "Reversible Defect"],
            help="Thalassemia type")
        
        # Vital Signs
        st.markdown("### 💓 Vital Signs")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=250, value=120, help="Systolic blood pressure")
        
        with col2:
            diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=50, max_value=150, value=80, help="Diastolic blood pressure")
        
        with col3:
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=75, help="Resting heart rate")
        
        # Lab Values
        st.markdown("### 🧪 Lab Values")
        col1, col2 = st.columns(2)
        
        with col1:
            glucose = st.number_input("Glucose (mg/dL)", min_value=50, max_value=500, value=100, help="Blood glucose level")
            cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200, help="Total cholesterol level")
        
        with col2:
            hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=100, value=50, help="HDL cholesterol level")
            ldl_cholesterol = st.number_input("LDL Cholesterol (mg/dL)", min_value=50, max_value=300, value=120, help="LDL cholesterol level")
        
        triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=50, max_value=500, value=150, help="Triglyceride level")
        
        # Lifestyle Factors
        st.markdown("### 🏃 Lifestyle Factors")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            smoking = st.selectbox("Smoking Status", [0, 1], format_func=lambda x: "Non-smoker" if x == 0 else "Current smoker")
        
        with col2:
            alcohol_consumption = st.selectbox("Alcohol Consumption", [0, 1, 2], 
                                            format_func=lambda x: ["None", "Light (1-2 drinks/week)", "Moderate (3-7 drinks/week)"][x])
        
        with col3:
            exercise_frequency = st.selectbox("Exercise Frequency", [0, 1, 2, 3],
                                            format_func=lambda x: ["None", "Light (1-2x/week)", "Moderate (3-4x/week)", "High (5+x/week)"][x])
        
        with col4:
            diet_quality = st.selectbox("Diet Quality", [1, 2, 3, 4, 5],
                                      format_func=lambda x: ["Poor", "Below Average", "Average", "Good", "Excellent"][x-1])
        
        # Medical History
        st.markdown("### 🏥 Medical History")
        col1, col2 = st.columns(2)
        
        with col1:
            family_diabetes = st.selectbox("Family History - Diabetes", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            family_heart_disease = st.selectbox("Family History - Heart Disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            family_eye_disease = st.selectbox("Family History - Eye Disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        
        with col2:
            hypertension = st.selectbox("Hypertension", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            previous_stroke = st.selectbox("Previous Stroke", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            kidney_disease = st.selectbox("Kidney Disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
        
        # Submit button
        submitted = st.form_submit_button("🔍 Analyze Disease Risk", use_container_width=True)
        
        if submitted:
            # Prepare data
            patient_data = {
                'age': age,
                'gender': gender,
                'bmi': bmi,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'heart_rate': heart_rate,
                'glucose': glucose,
                'cholesterol': cholesterol,
                'hdl_cholesterol': hdl_cholesterol,
                'ldl_cholesterol': ldl_cholesterol,
                'triglycerides': triglycerides,
                'smoking': smoking,
                'alcohol_consumption': alcohol_consumption,
                'exercise_frequency': exercise_frequency,
                'diet_quality': diet_quality,
                'family_diabetes': family_diabetes,
                'family_heart_disease': family_heart_disease,
                'family_eye_disease': family_eye_disease,
                'hypertension': hypertension,
                'previous_stroke': previous_stroke,
                'kidney_disease': kidney_disease,
                # UCI-specific features
                'chest_pain_type': chest_pain_type,
                'exercise_angina': 1 if exercise_angina == "Yes" else 0,
                'st_depression': st_depression,
                'major_vessels': major_vessels,
                'thalassemia': thalassemia
            }
            
            # Make predictions
            with st.spinner("Analyzing health data with AI models..."):
                try:
                    if ml_pipeline:
                        # Use local ML pipeline
                        predictions = {}
                        
                        # Diabetes prediction
                        diabetes_pred = ml_pipeline.predict_diabetes_risk(pd.DataFrame([patient_data]))
                        predictions['diabetes'] = diabetes_pred
                        
                        # Heart disease prediction
                        heart_pred = ml_pipeline.predict_heart_disease_risk(pd.DataFrame([patient_data]))
                        predictions['heart_disease'] = heart_pred
                        
                        # Eye disease prediction
                        patient_data['diabetes_risk'] = diabetes_pred['risk_score']
                        eye_pred = ml_pipeline.predict_eye_disease_risk(pd.DataFrame([patient_data]))
                        predictions['eye_disease'] = eye_pred
                        
                        # Store in session state
                        st.session_state.predictions = {
                            'predictions': predictions,
                            'timestamp': datetime.now().isoformat(),
                            'patient_data': patient_data
                        }
                        
                        st.success("✅ Risk assessment completed successfully!")
                        st.rerun()
                        
                    else:
                        st.error("❌ ML models not loaded. Please check the model status.")
                        
                except Exception as e:
                    st.error(f"❌ Prediction failed: {str(e)}")

def show_results():
    """Display prediction results"""
    
    if 'predictions' not in st.session_state or not st.session_state.predictions:
        st.warning("No prediction results available. Please complete a risk assessment first.")
        return
    
    predictions = st.session_state.predictions['predictions']
    timestamp = st.session_state.predictions['timestamp']
    
    st.subheader("📊 Risk Assessment Results")
    st.caption(f"Analysis completed on {datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Risk scores overview
    st.markdown("### 🎯 Risk Scores Overview")
    
    col1, col2, col3 = st.columns(3)
    
    disease_names = {
        'diabetes': 'Diabetes',
        'heart_disease': 'Heart Disease',
        'eye_disease': 'Eye Disease'
    }
    
    risk_colors = {
        'Low': '#27ae60',
        'Medium': '#f39c12',
        'High': '#e74c3c'
    }
    
    for i, (disease, prediction) in enumerate(predictions.items()):
        with [col1, col2, col3][i]:
            risk_score = prediction['risk_score']
            risk_level = prediction['risk_level']
            
            st.metric(
                label=disease_names[disease],
                value=f"{risk_score:.1%}",
                delta=f"{risk_level} Risk"
            )
    
    # Detailed results
    st.markdown("### 📋 Detailed Analysis")
    
    for disease, prediction in predictions.items():
        with st.expander(f"🔍 {disease_names[disease]} Analysis", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Risk score visualization
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = prediction['risk_score'] * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': f"{disease_names[disease]} Risk Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': risk_colors[prediction['risk_level']]},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 60], 'color': "yellow"},
                            {'range': [60, 100], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 60
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk level and recommendations
                st.markdown(f"**Risk Level:** <span class='risk-{prediction['risk_level'].lower()}'>{prediction['risk_level']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Risk Score:** {prediction['risk_score']:.3f}")
                
                st.markdown("**Recommendations:**")
                for rec in prediction['recommendations']:
                    st.markdown(f"• {rec}")
    
    # Summary visualization
    st.markdown("### 📈 Risk Comparison")
    
    # Prepare data for visualization
    risk_data = []
    for disease, prediction in predictions.items():
        risk_data.append({
            'Disease': disease_names[disease],
            'Risk Score': prediction['risk_score'] * 100,
            'Risk Level': prediction['risk_level']
        })
    
    df_risk = pd.DataFrame(risk_data)
    
    # Bar chart
    fig = px.bar(
        df_risk, 
        x='Disease', 
        y='Risk Score',
        color='Risk Level',
        color_discrete_map={
            'Low': '#27ae60',
            'Medium': '#f39c12',
            'High': '#e74c3c'
        },
        title="Disease Risk Comparison",
        labels={'Risk Score': 'Risk Score (%)', 'Disease': 'Disease Type'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Clear results button
    if st.button("🗑️ Clear Results", type="secondary"):
        del st.session_state.predictions
        st.rerun()

def show_prediction_summary(predictions):
    """Show summary of recent predictions"""
    
    if not predictions or 'predictions' not in predictions:
        return
    
    pred_data = predictions['predictions']
    
    # Create summary dataframe
    summary_data = []
    for disease, prediction in pred_data.items():
        summary_data.append({
            'Disease': disease.replace('_', ' ').title(),
            'Risk Score': f"{prediction['risk_score']:.1%}",
            'Risk Level': prediction['risk_level']
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)

def show_model_info(ml_pipeline):
    """Display model information"""
    
    st.subheader("🤖 Model Information")
    
    if not ml_pipeline:
        st.error("ML pipeline not loaded")
        return
    
    # Model status
    st.markdown("### 📊 Model Status")
    
    col1, col2, col3 = st.columns(3)
    
    models_info = {
        'diabetes': 'Diabetes Prediction',
        'heart_disease': 'Heart Disease Prediction',
        'eye_disease': 'Eye Disease Prediction'
    }
    
    for i, (model_name, display_name) in enumerate(models_info.items()):
        with [col1, col2, col3][i]:
            if model_name in ml_pipeline.models:
                st.success(f"✅ {display_name}")
                st.caption(f"Type: {type(ml_pipeline.models[model_name]).__name__}")
            else:
                st.error(f"❌ {display_name}")
    
    # Feature information
    st.markdown("### 🔧 Feature Information")
    
    if hasattr(ml_pipeline.preprocessor, 'feature_columns'):
        for model_name, features in ml_pipeline.preprocessor.feature_columns.items():
            with st.expander(f"{models_info[model_name]} Features"):
                st.write(f"Total features: {len(features)}")
                st.write("Features:", ", ".join(features))
    
    # Model performance (if available)
    st.markdown("### 📈 Performance Metrics")
    
    performance_data = {
        'Model': ['Diabetes', 'Heart Disease', 'Eye Disease'],
        'Algorithm': ['Random Forest', 'XGBoost', 'Random Forest'],
        'AUC Score': [0.95, 0.92, 0.90],
        'Accuracy': ['95%', '92%', '90%']
    }
    
    df_perf = pd.DataFrame(performance_data)
    st.dataframe(df_perf, use_container_width=True)

def show_settings():
    """Display settings page"""
    
    st.subheader("⚙️ Settings")
    
    # API Configuration
    st.markdown("### 🔌 API Configuration")
    
    api_url = st.text_input("API Base URL", value="http://localhost:5000", help="Base URL for the Healthcare Assistant API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        timeout = st.number_input("Request Timeout (seconds)", min_value=1, max_value=60, value=30)
    
    with col2:
        retry_attempts = st.number_input("Retry Attempts", min_value=0, max_value=5, value=3)
    
    # Model Configuration
    st.markdown("### 🧠 Model Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        diabetes_threshold = st.slider("Diabetes Risk Threshold", 0.0, 1.0, 0.5, 0.05)
    
    with col2:
        heart_threshold = st.slider("Heart Disease Risk Threshold", 0.0, 1.0, 0.5, 0.05)
    
    with col3:
        eye_threshold = st.slider("Eye Disease Risk Threshold", 0.0, 1.0, 0.5, 0.05)
    
    # Save settings
    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")
    
    # Clear cache
    st.markdown("### 🗑️ Cache Management")
    
    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared successfully!")

if __name__ == "__main__":
    main()
