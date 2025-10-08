import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.utils import resample
import xgboost as xgb
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_preprocessing import HealthDataPreprocessor

class HealthcareMLPipeline:
    """Machine Learning pipeline for healthcare disease prediction"""
    
    def __init__(self):
        self.models = {}
        self.preprocessor = HealthDataPreprocessor()
        self.model_path = 'models/'
        os.makedirs(self.model_path, exist_ok=True)
        
        # Load existing preprocessors if available
        self.preprocessor.load_preprocessors(self.model_path)
    
    def train_diabetes_model(self, X, y, test_size=0.2, random_state=42):
        """Train models for diabetes prediction"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Handle class imbalance
        X_train, y_train = self._handle_imbalance(X_train, y_train)
        
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=random_state,
                eval_metric='logloss'
            ),
            'logistic_regression': LogisticRegression(
                random_state=random_state,
                class_weight='balanced',
                max_iter=1000
            )
        }
        
        # Train and evaluate models
        results = {}
        for name, model in models.items():
            print(f"Training {name} for diabetes prediction...")
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            auc_score = roc_auc_score(y_test, y_pred_proba)
            results[name] = {
                'model': model,
                'auc_score': auc_score,
                'y_test': y_test,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"{name} AUC Score: {auc_score:.4f}")
        
        # Save best model
        best_model_name = max(results.keys(), key=lambda x: results[x]['auc_score'])
        self.models['diabetes'] = results[best_model_name]['model']
        
        # Save model
        joblib.dump(self.models['diabetes'], f"{self.model_path}/diabetes_model.pkl")
        
        return results, X_test, y_test
    
    def train_heart_disease_model(self, X, y, test_size=0.2, random_state=42):
        """Train models for heart disease prediction"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Handle class imbalance
        X_train, y_train = self._handle_imbalance(X_train, y_train)
        
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=150,
                max_depth=12,
                min_samples_split=4,
                min_samples_leaf=2,
                random_state=random_state,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=150,
                max_depth=7,
                learning_rate=0.08,
                subsample=0.85,
                colsample_bytree=0.85,
                random_state=random_state,
                eval_metric='logloss'
            ),
            'logistic_regression': LogisticRegression(
                random_state=random_state,
                class_weight='balanced',
                max_iter=1000,
                C=0.1
            )
        }
        
        # Train and evaluate models
        results = {}
        for name, model in models.items():
            print(f"Training {name} for heart disease prediction...")
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            auc_score = roc_auc_score(y_test, y_pred_proba)
            results[name] = {
                'model': model,
                'auc_score': auc_score,
                'y_test': y_test,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"{name} AUC Score: {auc_score:.4f}")
        
        # Save best model
        best_model_name = max(results.keys(), key=lambda x: results[x]['auc_score'])
        self.models['heart_disease'] = results[best_model_name]['model']
        
        # Save model
        joblib.dump(self.models['heart_disease'], f"{self.model_path}/heart_disease_model.pkl")
        
        return results, X_test, y_test
    
    def train_eye_disease_model(self, X, y, test_size=0.2, random_state=42):
        """Train models for eye disease prediction"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Handle class imbalance
        X_train, y_train = self._handle_imbalance(X_train, y_train)
        
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=120,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=random_state,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=120,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=random_state,
                eval_metric='logloss'
            ),
            'logistic_regression': LogisticRegression(
                random_state=random_state,
                class_weight='balanced',
                max_iter=1000,
                C=0.2
            )
        }
        
        # Train and evaluate models
        results = {}
        for name, model in models.items():
            print(f"Training {name} for eye disease prediction...")
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            auc_score = roc_auc_score(y_test, y_pred_proba)
            results[name] = {
                'model': model,
                'auc_score': auc_score,
                'y_test': y_test,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"{name} AUC Score: {auc_score:.4f}")
        
        # Save best model
        best_model_name = max(results.keys(), key=lambda x: results[x]['auc_score'])
        self.models['eye_disease'] = results[best_model_name]['model']
        
        # Save model
        joblib.dump(self.models['eye_disease'], f"{self.model_path}/eye_disease_model.pkl")
        
        return results, X_test, y_test
    
    def _handle_imbalance(self, X, y):
        """Handle class imbalance using SMOTE"""
        from imblearn.over_sampling import SMOTE
        
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        
        return X_resampled, y_resampled
    
    def train_all_models(self, n_samples=5000, use_real_data=True):
        """Train all disease prediction models"""
        if use_real_data:
            print("Loading real UCI Heart Disease dataset...")
            df = self.preprocessor.load_real_data(use_uci_heart=True, n_samples=n_samples)
        else:
            print("Creating synthetic healthcare data...")
            df = self.preprocessor.create_synthetic_data(n_samples)
        
        print("\nTraining Diabetes Prediction Model...")
        X_diabetes, y_diabetes, _ = self.preprocessor.preprocess_for_diabetes(df)
        diabetes_results, _, _ = self.train_diabetes_model(X_diabetes, y_diabetes)
        
        print("\nTraining Heart Disease Prediction Model...")
        X_heart, y_heart, _ = self.preprocessor.preprocess_for_heart_disease(df)
        heart_results, _, _ = self.train_heart_disease_model(X_heart, y_heart)
        
        print("\nTraining Eye Disease Prediction Model...")
        X_eye, y_eye, _ = self.preprocessor.preprocess_for_eye_disease(df)
        eye_results, _, _ = self.train_eye_disease_model(X_eye, y_eye)
        
        # Save preprocessors
        self.preprocessor.save_preprocessors()
        
        return {
            'diabetes': diabetes_results,
            'heart_disease': heart_results,
            'eye_disease': eye_results
        }
    
    def load_models(self):
        """Load trained models from disk"""
        for disease_type in ['diabetes', 'heart_disease', 'eye_disease']:
            model_path = f"{self.model_path}/{disease_type}_model.pkl"
            if os.path.exists(model_path):
                self.models[disease_type] = joblib.load(model_path)
                print(f"Loaded {disease_type} model")
        
        # Load preprocessors
        self.preprocessor.load_preprocessors()
    
    def predict_diabetes_risk(self, patient_data):
        """Predict diabetes risk for a patient"""
        if 'diabetes' not in self.models:
            raise ValueError("Diabetes model not loaded. Please train or load the model first.")
        
        # Transform data
        X_scaled = self.preprocessor.transform_new_data(patient_data, 'diabetes')
        
        # Predict
        risk_score = self.models['diabetes'].predict_proba(X_scaled)[0, 1]
        risk_level = self._get_risk_level(risk_score, 'diabetes')
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'recommendations': self._get_recommendations(risk_score, 'diabetes')
        }
    
    def predict_heart_disease_risk(self, patient_data):
        """Predict heart disease risk for a patient"""
        if 'heart_disease' not in self.models:
            raise ValueError("Heart disease model not loaded. Please train or load the model first.")
        
        # Transform data
        X_scaled = self.preprocessor.transform_new_data(patient_data, 'heart_disease')
        
        # Predict
        risk_score = self.models['heart_disease'].predict_proba(X_scaled)[0, 1]
        risk_level = self._get_risk_level(risk_score, 'heart_disease')
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'recommendations': self._get_recommendations(risk_score, 'heart_disease')
        }
    
    def predict_eye_disease_risk(self, patient_data):
        """Predict eye disease risk for a patient"""
        if 'eye_disease' not in self.models:
            raise ValueError("Eye disease model not loaded. Please train or load the model first.")
        
        # Transform data
        X_scaled = self.preprocessor.transform_new_data(patient_data, 'eye_disease')
        
        # Predict
        risk_score = self.models['eye_disease'].predict_proba(X_scaled)[0, 1]
        risk_level = self._get_risk_level(risk_score, 'eye_disease')
        
        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'recommendations': self._get_recommendations(risk_score, 'eye_disease')
        }
    
    def _get_risk_level(self, risk_score, disease_type):
        """Convert risk score to risk level"""
        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        else:
            return "High"
    
    def _get_recommendations(self, risk_score, disease_type):
        """Generate personalized recommendations based on risk score"""
        recommendations = []
        
        if disease_type == 'diabetes':
            if risk_score > 0.6:
                recommendations.extend([
                    "Schedule regular blood glucose monitoring",
                    "Consult with an endocrinologist",
                    "Maintain a low-carb diet",
                    "Exercise regularly (30+ minutes daily)"
                ])
            elif risk_score > 0.3:
                recommendations.extend([
                    "Monitor blood glucose levels",
                    "Maintain healthy diet",
                    "Regular physical activity",
                    "Annual diabetes screening"
                ])
            else:
                recommendations.extend([
                    "Maintain current healthy lifestyle",
                    "Annual health checkup",
                    "Continue balanced diet"
                ])
        
        elif disease_type == 'heart_disease':
            if risk_score > 0.6:
                recommendations.extend([
                    "Immediate cardiologist consultation",
                    "Regular blood pressure monitoring",
                    "Low-sodium, heart-healthy diet",
                    "Quit smoking if applicable",
                    "Regular exercise program"
                ])
            elif risk_score > 0.3:
                recommendations.extend([
                    "Monitor blood pressure and cholesterol",
                    "Heart-healthy diet",
                    "Regular exercise",
                    "Annual cardiac screening"
                ])
            else:
                recommendations.extend([
                    "Maintain healthy lifestyle",
                    "Regular exercise",
                    "Annual health checkup"
                ])
        
        elif disease_type == 'eye_disease':
            if risk_score > 0.6:
                recommendations.extend([
                    "Immediate ophthalmologist consultation",
                    "Regular eye exams (every 6 months)",
                    "Control blood sugar and blood pressure",
                    "Protect eyes from UV light"
                ])
            elif risk_score > 0.3:
                recommendations.extend([
                    "Annual comprehensive eye exam",
                    "Monitor blood sugar levels",
                    "Maintain healthy blood pressure",
                    "Wear UV-protective sunglasses"
                ])
            else:
                recommendations.extend([
                    "Regular eye exams (every 2 years)",
                    "Maintain overall health",
                    "Protect eyes from UV light"
                ])
        
        return recommendations

def main():
    """Main function to train and save models"""
    pipeline = HealthcareMLPipeline()
    
    print("Starting Healthcare ML Pipeline Training...")
    results = pipeline.train_all_models(n_samples=10000)
    
    print("\nTraining completed successfully!")
    print("Models saved to 'models/' directory")
    
    # Print summary
    for disease, models in results.items():
        print(f"\n{disease.replace('_', ' ').title()} Results:")
        for model_name, result in models.items():
            print(f"  {model_name}: AUC = {result['auc_score']:.4f}")

if __name__ == "__main__":
    main()
