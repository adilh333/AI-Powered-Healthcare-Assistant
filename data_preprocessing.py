import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import joblib
import os
from data_loader import UCIHeartDiseaseLoader

class HealthDataPreprocessor:
    """Handles data preprocessing for healthcare prediction models"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = {}
        
    def load_real_data(self, use_uci_heart=True, n_samples=5000):
        """Load real healthcare datasets"""
        if use_uci_heart:
            print("📊 Loading UCI Heart Disease Dataset...")
            loader = UCIHeartDiseaseLoader()
            
            # Download and process data
            if not os.path.exists(f"{loader.data_path}/heart_disease_cleaned.csv"):
                if not loader.download_data():
                    print("❌ Failed to download UCI dataset, falling back to synthetic data")
                    return self.create_synthetic_data(n_samples)
                
                df = loader.load_and_clean_data()
                if df is None:
                    print("❌ Failed to process UCI dataset, falling back to synthetic data")
                    return self.create_synthetic_data(n_samples)
            else:
                df = pd.read_csv(f"{loader.data_path}/heart_disease_cleaned.csv")
            
            # Create extended dataset
            extended_df = loader.create_extended_dataset(df, n_samples)
            
            # Map UCI features to our standard format
            df_mapped = self._map_uci_to_standard_format(extended_df)
            
            return df_mapped
        else:
            return self.create_synthetic_data(n_samples)
    
    def _map_uci_to_standard_format(self, df):
        """Map UCI Heart Disease features to standard healthcare format"""
        # Create a new dataframe with standard features
        mapped_df = pd.DataFrame()
        
        # Direct mappings
        mapped_df['age'] = df['age']
        mapped_df['gender'] = df['sex']
        mapped_df['systolic_bp'] = df['trestbps']  # Resting blood pressure
        mapped_df['heart_rate'] = df['thalach']    # Max heart rate achieved
        mapped_df['cholesterol'] = df['chol']      # Serum cholesterol
        
        # Create derived features
        # BMI estimation (rough approximation)
        mapped_df['bmi'] = np.random.normal(25, 5, len(df))
        
        # Diastolic BP estimation from systolic
        mapped_df['diastolic_bp'] = mapped_df['systolic_bp'] * 0.6 + np.random.normal(0, 5, len(df))
        
        # Glucose levels (not in UCI dataset, so estimate)
        mapped_df['glucose'] = np.random.normal(100, 30, len(df))
        mapped_df['fbs_high'] = df['fbs'].map({'High': 1, 'Normal': 0})
        
        # Cholesterol breakdown (estimate from total)
        mapped_df['hdl_cholesterol'] = np.random.normal(50, 15, len(df))
        mapped_df['ldl_cholesterol'] = mapped_df['cholesterol'] - mapped_df['hdl_cholesterol'] - 50
        mapped_df['triglycerides'] = np.random.normal(150, 80, len(df))
        
        # Lifestyle factors (not in UCI dataset, so estimate)
        mapped_df['smoking'] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
        mapped_df['alcohol_consumption'] = np.random.choice([0, 1, 2], len(df), p=[0.4, 0.4, 0.2])
        mapped_df['exercise_frequency'] = np.random.choice([0, 1, 2, 3], len(df), p=[0.2, 0.3, 0.3, 0.2])
        mapped_df['diet_quality'] = np.random.choice([1, 2, 3, 4, 5], len(df))
        
        # Family history (not in UCI dataset, so estimate)
        mapped_df['family_diabetes'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])
        mapped_df['family_heart_disease'] = np.random.choice([0, 1], len(df), p=[0.85, 0.15])
        mapped_df['family_eye_disease'] = np.random.choice([0, 1], len(df), p=[0.9, 0.1])
        
        # Medical history from UCI features
        mapped_df['hypertension'] = (mapped_df['systolic_bp'] > 140).astype(int)
        mapped_df['previous_stroke'] = np.random.choice([0, 1], len(df), p=[0.95, 0.05])
        mapped_df['kidney_disease'] = np.random.choice([0, 1], len(df), p=[0.95, 0.05])
        
        # UCI-specific features (keep as strings for now, will be encoded during preprocessing)
        mapped_df['chest_pain_type'] = df['cp']
        mapped_df['exercise_angina'] = df['exang'].map({'Yes': 1, 'No': 0})
        mapped_df['st_depression'] = df['oldpeak']
        mapped_df['major_vessels'] = df['ca']
        mapped_df['thalassemia'] = df['thal']
        
        # Create target variables
        mapped_df['heart_disease_risk'] = df['target']  # Direct from UCI
        mapped_df['diabetes_risk'] = self._estimate_diabetes_risk(mapped_df)
        mapped_df['eye_disease_risk'] = self._estimate_eye_disease_risk(mapped_df)
        
        return mapped_df
    
    def _estimate_diabetes_risk(self, df):
        """Estimate diabetes risk based on available features"""
        risk = (
            (df['glucose'] - 100) * 0.02 +
            (df['bmi'] - 25) * 0.05 +
            (df['age'] - 40) * 0.01 +
            df['family_diabetes'] * 0.3 +
            df['hypertension'] * 0.2 +
            df['fbs_high'] * 0.4 +
            np.random.normal(0, 0.1, len(df))
        )
        return (risk > 0.5).astype(int)
    
    def _estimate_eye_disease_risk(self, df):
        """Estimate eye disease risk based on available features"""
        risk = (
            df['diabetes_risk'] * 0.6 +
            (df['age'] - 60) * 0.02 +
            df['hypertension'] * 0.3 +
            df['family_eye_disease'] * 0.4 +
            (df['glucose'] - 100) * 0.001 +
            np.random.normal(0, 0.1, len(df))
        )
        return (risk > 0.4).astype(int)

    def create_synthetic_data(self, n_samples=10000):
        """Create synthetic healthcare data for demonstration"""
        np.random.seed(42)
        
        data = {
            # Basic Demographics
            'age': np.random.normal(45, 15, n_samples).astype(int),
            'gender': np.random.choice(['Male', 'Female'], n_samples),
            'bmi': np.random.normal(25, 5, n_samples),
            
            # Vital Signs
            'systolic_bp': np.random.normal(120, 20, n_samples),
            'diastolic_bp': np.random.normal(80, 15, n_samples),
            'heart_rate': np.random.normal(75, 15, n_samples),
            
            # Lab Values
            'glucose': np.random.normal(100, 30, n_samples),
            'cholesterol': np.random.normal(200, 50, n_samples),
            'hdl_cholesterol': np.random.normal(50, 15, n_samples),
            'ldl_cholesterol': np.random.normal(120, 40, n_samples),
            'triglycerides': np.random.normal(150, 80, n_samples),
            
            # Lifestyle Factors
            'smoking': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'alcohol_consumption': np.random.choice([0, 1, 2], n_samples, p=[0.4, 0.4, 0.2]),
            'exercise_frequency': np.random.choice([0, 1, 2, 3], n_samples, p=[0.2, 0.3, 0.3, 0.2]),
            'diet_quality': np.random.choice([1, 2, 3, 4, 5], n_samples),
            
            # Family History
            'family_diabetes': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'family_heart_disease': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
            'family_eye_disease': np.random.choice([0, 1], n_samples, p=[0.9, 0.1]),
            
            # Medical History
            'hypertension': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'previous_stroke': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
            'kidney_disease': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        }
        
        df = pd.DataFrame(data)
        
        # Create realistic correlations and target variables
        df = self._create_target_variables(df)
        
        return df
    
    def _create_target_variables(self, df):
        """Create realistic target variables based on health factors"""
        
        # Diabetes risk based on glucose, BMI, age, family history
        diabetes_risk = (
            (df['glucose'] - 100) * 0.02 +
            (df['bmi'] - 25) * 0.05 +
            (df['age'] - 40) * 0.01 +
            df['family_diabetes'] * 0.3 +
            df['hypertension'] * 0.2 +
            np.random.normal(0, 0.1, len(df))
        )
        df['diabetes_risk'] = (diabetes_risk > 0.5).astype(int)
        
        # Heart disease risk based on cholesterol, BP, age, lifestyle
        heart_risk = (
            (df['cholesterol'] - 200) * 0.001 +
            (df['systolic_bp'] - 120) * 0.005 +
            (df['age'] - 50) * 0.02 +
            df['family_heart_disease'] * 0.4 +
            df['smoking'] * 0.3 +
            (df['exercise_frequency'] == 0) * 0.2 +
            np.random.normal(0, 0.1, len(df))
        )
        df['heart_disease_risk'] = (heart_risk > 0.3).astype(int)
        
        # Eye disease risk based on diabetes, age, hypertension
        eye_risk = (
            df['diabetes_risk'] * 0.6 +
            (df['age'] - 60) * 0.02 +
            df['hypertension'] * 0.3 +
            df['family_eye_disease'] * 0.4 +
            (df['glucose'] - 100) * 0.001 +
            np.random.normal(0, 0.1, len(df))
        )
        df['eye_disease_risk'] = (eye_risk > 0.4).astype(int)
        
        return df
    
    def preprocess_for_diabetes(self, df):
        """Preprocess data specifically for diabetes prediction"""
        # Check if this is UCI data (has UCI-specific features)
        if 'chest_pain_type' in df.columns:
            # UCI data - use available features (exclude string categoricals for now)
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_diabetes', 'hypertension', 'previous_stroke', 'kidney_disease',
                'exercise_angina', 'st_depression', 'major_vessels'
            ]
        else:
            # Synthetic data - use standard features
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_diabetes', 'hypertension', 'previous_stroke', 'kidney_disease'
            ]
        
        # Encode categorical variables
        df_processed = df.copy()
        df_processed['gender_encoded'] = LabelEncoder().fit_transform(df_processed['gender'])
        feature_cols.append('gender_encoded')
        
        # Encode UCI-specific categorical variables if present
        if 'chest_pain_type' in df_processed.columns:
            df_processed['chest_pain_type_encoded'] = LabelEncoder().fit_transform(df_processed['chest_pain_type'])
            df_processed['thalassemia_encoded'] = LabelEncoder().fit_transform(df_processed['thalassemia'])
            feature_cols.extend(['chest_pain_type_encoded', 'thalassemia_encoded'])
        
        X = df_processed[feature_cols]
        y = df_processed['diabetes_risk']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        self.scalers['diabetes'] = scaler
        self.feature_columns['diabetes'] = feature_cols
        
        return X_scaled, y, feature_cols
    
    def preprocess_for_heart_disease(self, df):
        """Preprocess data specifically for heart disease prediction"""
        # Check if this is UCI data (has UCI-specific features)
        if 'chest_pain_type' in df.columns:
            # UCI data - use available features (exclude string categoricals for now)
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_heart_disease', 'hypertension', 'previous_stroke', 'kidney_disease',
                'exercise_angina', 'st_depression', 'major_vessels'
            ]
        else:
            # Synthetic data - use standard features
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_heart_disease', 'hypertension', 'previous_stroke', 'kidney_disease'
            ]
        
        # Encode categorical variables
        df_processed = df.copy()
        df_processed['gender_encoded'] = LabelEncoder().fit_transform(df_processed['gender'])
        feature_cols.append('gender_encoded')
        
        # Encode UCI-specific categorical variables if present
        if 'chest_pain_type' in df_processed.columns:
            df_processed['chest_pain_type_encoded'] = LabelEncoder().fit_transform(df_processed['chest_pain_type'])
            df_processed['thalassemia_encoded'] = LabelEncoder().fit_transform(df_processed['thalassemia'])
            feature_cols.extend(['chest_pain_type_encoded', 'thalassemia_encoded'])
        
        X = df_processed[feature_cols]
        y = df_processed['heart_disease_risk']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        self.scalers['heart_disease'] = scaler
        self.feature_columns['heart_disease'] = feature_cols
        
        return X_scaled, y, feature_cols
    
    def preprocess_for_eye_disease(self, df):
        """Preprocess data specifically for eye disease prediction"""
        # Check if this is UCI data (has UCI-specific features)
        if 'chest_pain_type' in df.columns:
            # UCI data - use available features (exclude string categoricals for now)
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_eye_disease', 'hypertension', 'previous_stroke', 'kidney_disease',
                'diabetes_risk',  # Include diabetes as a feature for eye disease
                'exercise_angina', 'st_depression', 'major_vessels'
            ]
        else:
            # Synthetic data - use standard features
            feature_cols = [
                'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'glucose',
                'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
                'smoking', 'alcohol_consumption', 'exercise_frequency', 'diet_quality',
                'family_eye_disease', 'hypertension', 'previous_stroke', 'kidney_disease',
                'diabetes_risk'  # Include diabetes as a feature for eye disease
            ]
        
        # Encode categorical variables
        df_processed = df.copy()
        df_processed['gender_encoded'] = LabelEncoder().fit_transform(df_processed['gender'])
        feature_cols.append('gender_encoded')
        
        # Encode UCI-specific categorical variables if present
        if 'chest_pain_type' in df_processed.columns:
            df_processed['chest_pain_type_encoded'] = LabelEncoder().fit_transform(df_processed['chest_pain_type'])
            df_processed['thalassemia_encoded'] = LabelEncoder().fit_transform(df_processed['thalassemia'])
            feature_cols.extend(['chest_pain_type_encoded', 'thalassemia_encoded'])
        
        X = df_processed[feature_cols]
        y = df_processed['eye_disease_risk']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        self.scalers['eye_disease'] = scaler
        self.feature_columns['eye_disease'] = feature_cols
        
        return X_scaled, y, feature_cols
    
    def save_preprocessors(self, model_path='models/'):
        """Save preprocessors for later use"""
        os.makedirs(model_path, exist_ok=True)
        
        for model_type, scaler in self.scalers.items():
            joblib.dump(scaler, f"{model_path}/{model_type}_scaler.pkl")
        
        joblib.dump(self.feature_columns, f"{model_path}/feature_columns.pkl")
    
    def load_preprocessors(self, model_path='models/'):
        """Load preprocessors from disk"""
        self.scalers = {}
        for model_type in ['diabetes', 'heart_disease', 'eye_disease']:
            scaler_path = f"{model_path}/{model_type}_scaler.pkl"
            if os.path.exists(scaler_path):
                self.scalers[model_type] = joblib.load(scaler_path)
        
        feature_path = f"{model_path}/feature_columns.pkl"
        if os.path.exists(feature_path):
            self.feature_columns = joblib.load(feature_path)
    
    def transform_new_data(self, data, model_type):
        """Transform new data using saved preprocessors"""
        if model_type not in self.scalers:
            raise ValueError(f"No scaler found for {model_type}")
        
        # Create a copy to avoid modifying original data
        data_copy = data.copy()
        
        # Encode gender if present
        if 'gender' in data_copy.columns and 'gender_encoded' not in data_copy.columns:
            # Use a consistent mapping for gender encoding
            gender_mapping = {'Male': 1, 'Female': 0}
            data_copy['gender_encoded'] = data_copy['gender'].map(gender_mapping)
        
        # Encode UCI-specific categorical variables if present
        if 'chest_pain_type' in data_copy.columns and 'chest_pain_type_encoded' not in data_copy.columns:
            le = LabelEncoder()
            data_copy['chest_pain_type_encoded'] = le.fit_transform(data_copy['chest_pain_type'])
        
        if 'thalassemia' in data_copy.columns and 'thalassemia_encoded' not in data_copy.columns:
            le = LabelEncoder()
            data_copy['thalassemia_encoded'] = le.fit_transform(data_copy['thalassemia'])
        
        # Ensure data has all required features
        feature_cols = self.feature_columns[model_type]
        missing_features = set(feature_cols) - set(data_copy.columns)
        if missing_features:
            raise ValueError(f"Missing features: {missing_features}")
        
        # Select and scale features
        X = data_copy[feature_cols]
        X_scaled = self.scalers[model_type].transform(X)
        
        return X_scaled
