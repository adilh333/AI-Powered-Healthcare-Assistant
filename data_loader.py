"""
Data loader for UCI Heart Disease Dataset
Downloads and processes the real heart disease dataset from UCI ML Repository
"""

import pandas as pd
import numpy as np
import requests
import os
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import joblib

class UCIHeartDiseaseLoader:
    """Handles loading and preprocessing of UCI Heart Disease Dataset"""
    
    def __init__(self):
        self.data_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
        self.feature_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'
        ]
        self.data_path = 'data/'
        os.makedirs(self.data_path, exist_ok=True)
    
    def download_data(self):
        """Download the UCI Heart Disease dataset"""
        try:
            print("Downloading UCI Heart Disease dataset...")
            response = requests.get(self.data_url)
            response.raise_for_status()
            
            # Save raw data
            with open(f"{self.data_path}/heart_disease_raw.csv", 'w') as f:
                f.write(response.text)
            
            print("✅ Dataset downloaded successfully")
            return True
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def load_and_clean_data(self):
        """Load and clean the heart disease dataset"""
        try:
            # Read the data
            df = pd.read_csv(f"{self.data_path}/heart_disease_raw.csv", 
                           names=self.feature_names, 
                           na_values='?')
            
            print(f"📊 Loaded dataset with {len(df)} records and {len(df.columns)} features")
            
            # Handle missing values
            print("🧹 Cleaning data...")
            missing_before = df.isnull().sum().sum()
            
            # Fill missing values with median for numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
            
            # Fill missing values with mode for categorical columns
            categorical_columns = df.select_dtypes(include=['object']).columns
            for col in categorical_columns:
                df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'unknown')
            
            missing_after = df.isnull().sum().sum()
            print(f"   Removed {missing_before - missing_after} missing values")
            
            # Convert target to binary (0 = no disease, 1 = disease)
            df['target'] = (df['target'] > 0).astype(int)
            
            # Create binary features for better interpretation
            df['sex'] = df['sex'].map({1: 'Male', 0: 'Female'})
            df['fbs'] = df['fbs'].map({1: 'High', 0: 'Normal'})
            df['exang'] = df['exang'].map({1: 'Yes', 0: 'No'})
            
            # Chest pain type mapping
            cp_mapping = {1: 'Typical Angina', 2: 'Atypical Angina', 3: 'Non-anginal Pain', 4: 'Asymptomatic'}
            df['cp'] = df['cp'].map(cp_mapping)
            
            # Resting ECG mapping
            restecg_mapping = {0: 'Normal', 1: 'ST-T Abnormality', 2: 'Left Ventricular Hypertrophy'}
            df['restecg'] = df['restecg'].map(restecg_mapping)
            
            # Slope mapping
            slope_mapping = {1: 'Upsloping', 2: 'Flat', 3: 'Downsloping'}
            df['slope'] = df['slope'].map(slope_mapping)
            
            # Thalassemia mapping
            thal_mapping = {3: 'Normal', 6: 'Fixed Defect', 7: 'Reversible Defect'}
            df['thal'] = df['thal'].map(thal_mapping)
            
            # Save cleaned data
            df.to_csv(f"{self.data_path}/heart_disease_cleaned.csv", index=False)
            
            print("✅ Data cleaned and saved")
            print(f"📈 Target distribution: {df['target'].value_counts().to_dict()}")
            
            return df
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def create_extended_dataset(self, df, n_samples=5000):
        """Create an extended dataset by augmenting the real data"""
        print(f"🔄 Creating extended dataset with {n_samples} samples...")
        
        # Use SMOTE-like approach to generate synthetic samples
        from sklearn.neighbors import NearestNeighbors
        
        # Separate features and target
        X = df.drop('target', axis=1)
        y = df['target']
        
        # Get numeric columns for augmentation
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
        X_numeric = X[numeric_cols]
        
        # Generate synthetic samples
        synthetic_samples = []
        target_samples = []
        
        for class_label in y.unique():
            class_data = X_numeric[y == class_label]
            class_count = int(n_samples * (y == class_label).sum() / len(y))
            
            if len(class_data) > 1:
                # Use KNN to generate synthetic samples
                knn = NearestNeighbors(n_neighbors=min(3, len(class_data)-1))
                knn.fit(class_data)
                
                for _ in range(class_count):
                    # Pick a random sample
                    idx = np.random.randint(0, len(class_data))
                    sample = class_data.iloc[idx].values
                    
                    # Find neighbors
                    distances, indices = knn.kneighbors([sample])
                    
                    # Generate synthetic sample
                    neighbor_idx = np.random.choice(indices[0][1:])  # Exclude self
                    neighbor = class_data.iloc[neighbor_idx].values
                    
                    # Interpolate between sample and neighbor
                    alpha = np.random.random()
                    synthetic_sample = sample + alpha * (neighbor - sample)
                    
                    # Add some noise
                    noise = np.random.normal(0, 0.1, len(synthetic_sample))
                    synthetic_sample += noise
                    
                    synthetic_samples.append(synthetic_sample)
                    target_samples.append(class_label)
        
        # Create synthetic dataframe
        synthetic_df = pd.DataFrame(synthetic_samples, columns=numeric_cols)
        synthetic_df['target'] = target_samples
        
        # Add categorical features by sampling from original data
        categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
        for col in categorical_cols:
            synthetic_df[col] = np.random.choice(X[col].values, len(synthetic_df))
        
        # Combine original and synthetic data
        extended_df = pd.concat([df, synthetic_df], ignore_index=True)
        
        print(f"✅ Extended dataset created with {len(extended_df)} total samples")
        print(f"📈 Extended target distribution: {extended_df['target'].value_counts().to_dict()}")
        
        return extended_df
    
    def preprocess_for_ml(self, df):
        """Preprocess data for machine learning"""
        print("🔧 Preprocessing data for ML...")
        
        # Create a copy for preprocessing
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_columns = df_processed.select_dtypes(include=['object']).columns
        label_encoders = {}
        
        for col in categorical_columns:
            le = LabelEncoder()
            df_processed[col] = le.fit_transform(df_processed[col])
            label_encoders[col] = le
        
        # Separate features and target
        X = df_processed.drop('target', axis=1)
        y = df_processed['target']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Save preprocessors
        joblib.dump(scaler, f"{self.data_path}/heart_disease_scaler.pkl")
        joblib.dump(label_encoders, f"{self.data_path}/heart_disease_encoders.pkl")
        joblib.dump(X.columns.tolist(), f"{self.data_path}/heart_disease_features.pkl")
        
        print("✅ Data preprocessed and preprocessors saved")
        
        return X_scaled, y, X.columns.tolist(), label_encoders
    
    def get_feature_descriptions(self):
        """Get detailed feature descriptions"""
        return {
            'age': 'Age in years',
            'sex': 'Gender (Male/Female)',
            'cp': 'Chest pain type (Typical Angina, Atypical Angina, Non-anginal Pain, Asymptomatic)',
            'trestbps': 'Resting blood pressure (mm Hg)',
            'chol': 'Serum cholesterol (mg/dl)',
            'fbs': 'Fasting blood sugar > 120 mg/dl (High/Normal)',
            'restecg': 'Resting electrocardiographic results',
            'thalach': 'Maximum heart rate achieved',
            'exang': 'Exercise induced angina (Yes/No)',
            'oldpeak': 'ST depression induced by exercise relative to rest',
            'slope': 'Slope of the peak exercise ST segment',
            'ca': 'Number of major vessels colored by fluoroscopy',
            'thal': 'Thalassemia type',
            'target': 'Heart disease presence (0=No, 1=Yes)'
        }

def main():
    """Main function to download and process the dataset"""
    loader = UCIHeartDiseaseLoader()
    
    # Download data
    if not loader.download_data():
        return
    
    # Load and clean data
    df = loader.load_and_clean_data()
    if df is None:
        return
    
    # Create extended dataset
    extended_df = loader.create_extended_dataset(df, n_samples=5000)
    
    # Preprocess for ML
    X_scaled, y, feature_names, encoders = loader.preprocess_for_ml(extended_df)
    
    print("\n🎉 UCI Heart Disease Dataset processing completed!")
    print(f"📊 Final dataset shape: {X_scaled.shape}")
    print(f"🎯 Target distribution: {pd.Series(y).value_counts().to_dict()}")
    
    return extended_df, X_scaled, y, feature_names, encoders

if __name__ == "__main__":
    main()
