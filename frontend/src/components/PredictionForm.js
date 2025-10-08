import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const FormContainer = styled.div`
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
`;

const FormTitle = styled.h2`
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
  margin: 0 0 2rem 0;
  text-align: center;
`;

const FormGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const FormLabel = styled.label`
  color: #2c3e50;
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
`;

const FormInput = styled.input`
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const FormSelect = styled.select`
  padding: 0.75rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: border-color 0.3s ease;
  
  &:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
  display: block;
  
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoadingMessage = styled.div`
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
  padding: 2rem;
`;

const ErrorMessage = styled.div`
  background: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  border: 1px solid #fcc;
`;

const PredictionForm = ({ onPrediction, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    age: '',
    gender: 'Male',
    bmi: '',
    systolic_bp: '',
    diastolic_bp: '',
    heart_rate: '75',
    glucose: '',
    cholesterol: '',
    hdl_cholesterol: '',
    ldl_cholesterol: '',
    triglycerides: '',
    smoking: '0',
    alcohol_consumption: '0',
    exercise_frequency: '2',
    diet_quality: '3',
    family_diabetes: '0',
    family_heart_disease: '0',
    family_eye_disease: '0',
    hypertension: '0',
    previous_stroke: '0',
    kidney_disease: '0'
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    onLoading(true);

    try {
      // Convert string values to appropriate types
      const processedData = {
        ...formData,
        age: parseInt(formData.age),
        bmi: parseFloat(formData.bmi),
        systolic_bp: parseFloat(formData.systolic_bp),
        diastolic_bp: parseFloat(formData.diastolic_bp),
        heart_rate: parseInt(formData.heart_rate),
        glucose: parseFloat(formData.glucose),
        cholesterol: parseFloat(formData.cholesterol),
        hdl_cholesterol: parseFloat(formData.hdl_cholesterol),
        ldl_cholesterol: parseFloat(formData.ldl_cholesterol),
        triglycerides: parseFloat(formData.triglycerides),
        smoking: parseInt(formData.smoking),
        alcohol_consumption: parseInt(formData.alcohol_consumption),
        exercise_frequency: parseInt(formData.exercise_frequency),
        diet_quality: parseInt(formData.diet_quality),
        family_diabetes: parseInt(formData.family_diabetes),
        family_heart_disease: parseInt(formData.family_heart_disease),
        family_eye_disease: parseInt(formData.family_eye_disease),
        hypertension: parseInt(formData.hypertension),
        previous_stroke: parseInt(formData.previous_stroke),
        kidney_disease: parseInt(formData.kidney_disease)
      };

      const response = await axios.post('http://localhost:5000/predict/all', processedData);
      
      onPrediction(response.data);
      setLoading(false);
      onLoading(false);
    } catch (err) {
      const errorMessage = err.response?.data?.error || 'An error occurred during prediction';
      setError(errorMessage);
      onError(errorMessage);
      setLoading(false);
      onLoading(false);
    }
  };

  return (
    <FormContainer>
      <FormTitle>Health Risk Assessment</FormTitle>
      <p style={{ textAlign: 'center', color: '#7f8c8d', marginBottom: '2rem' }}>
        Please provide your health information for comprehensive disease risk assessment
      </p>

      <form onSubmit={handleSubmit}>
        <FormGrid>
          <FormGroup>
            <FormLabel>Age *</FormLabel>
            <FormInput
              type="number"
              name="age"
              value={formData.age}
              onChange={handleInputChange}
              required
              min="18"
              max="100"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Gender *</FormLabel>
            <FormSelect
              name="gender"
              value={formData.gender}
              onChange={handleInputChange}
              required
            >
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>BMI (Body Mass Index) *</FormLabel>
            <FormInput
              type="number"
              name="bmi"
              value={formData.bmi}
              onChange={handleInputChange}
              required
              min="15"
              max="50"
              step="0.1"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Systolic Blood Pressure (mmHg) *</FormLabel>
            <FormInput
              type="number"
              name="systolic_bp"
              value={formData.systolic_bp}
              onChange={handleInputChange}
              required
              min="80"
              max="250"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Diastolic Blood Pressure (mmHg) *</FormLabel>
            <FormInput
              type="number"
              name="diastolic_bp"
              value={formData.diastolic_bp}
              onChange={handleInputChange}
              required
              min="50"
              max="150"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Heart Rate (bpm)</FormLabel>
            <FormInput
              type="number"
              name="heart_rate"
              value={formData.heart_rate}
              onChange={handleInputChange}
              min="40"
              max="200"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Glucose Level (mg/dL) *</FormLabel>
            <FormInput
              type="number"
              name="glucose"
              value={formData.glucose}
              onChange={handleInputChange}
              required
              min="50"
              max="500"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Total Cholesterol (mg/dL) *</FormLabel>
            <FormInput
              type="number"
              name="cholesterol"
              value={formData.cholesterol}
              onChange={handleInputChange}
              required
              min="100"
              max="400"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>HDL Cholesterol (mg/dL) *</FormLabel>
            <FormInput
              type="number"
              name="hdl_cholesterol"
              value={formData.hdl_cholesterol}
              onChange={handleInputChange}
              required
              min="20"
              max="100"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>LDL Cholesterol (mg/dL) *</FormLabel>
            <FormInput
              type="number"
              name="ldl_cholesterol"
              value={formData.ldl_cholesterol}
              onChange={handleInputChange}
              required
              min="50"
              max="300"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Triglycerides (mg/dL) *</FormLabel>
            <FormInput
              type="number"
              name="triglycerides"
              value={formData.triglycerides}
              onChange={handleInputChange}
              required
              min="50"
              max="500"
            />
          </FormGroup>

          <FormGroup>
            <FormLabel>Smoking Status</FormLabel>
            <FormSelect
              name="smoking"
              value={formData.smoking}
              onChange={handleInputChange}
            >
              <option value="0">Non-smoker</option>
              <option value="1">Current smoker</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Alcohol Consumption</FormLabel>
            <FormSelect
              name="alcohol_consumption"
              value={formData.alcohol_consumption}
              onChange={handleInputChange}
            >
              <option value="0">None</option>
              <option value="1">Light (1-2 drinks/week)</option>
              <option value="2">Moderate (3-7 drinks/week)</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Exercise Frequency</FormLabel>
            <FormSelect
              name="exercise_frequency"
              value={formData.exercise_frequency}
              onChange={handleInputChange}
            >
              <option value="0">None</option>
              <option value="1">Light (1-2 times/week)</option>
              <option value="2">Moderate (3-4 times/week)</option>
              <option value="3">High (5+ times/week)</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Diet Quality (1-5 scale)</FormLabel>
            <FormSelect
              name="diet_quality"
              value={formData.diet_quality}
              onChange={handleInputChange}
            >
              <option value="1">Poor</option>
              <option value="2">Below Average</option>
              <option value="3">Average</option>
              <option value="4">Good</option>
              <option value="5">Excellent</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Family History - Diabetes</FormLabel>
            <FormSelect
              name="family_diabetes"
              value={formData.family_diabetes}
              onChange={handleInputChange}
            >
              <option value="0">No family history</option>
              <option value="1">Family history present</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Family History - Heart Disease</FormLabel>
            <FormSelect
              name="family_heart_disease"
              value={formData.family_heart_disease}
              onChange={handleInputChange}
            >
              <option value="0">No family history</option>
              <option value="1">Family history present</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Family History - Eye Disease</FormLabel>
            <FormSelect
              name="family_eye_disease"
              value={formData.family_eye_disease}
              onChange={handleInputChange}
            >
              <option value="0">No family history</option>
              <option value="1">Family history present</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Hypertension</FormLabel>
            <FormSelect
              name="hypertension"
              value={formData.hypertension}
              onChange={handleInputChange}
            >
              <option value="0">No</option>
              <option value="1">Yes</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Previous Stroke</FormLabel>
            <FormSelect
              name="previous_stroke"
              value={formData.previous_stroke}
              onChange={handleInputChange}
            >
              <option value="0">No</option>
              <option value="1">Yes</option>
            </FormSelect>
          </FormGroup>

          <FormGroup>
            <FormLabel>Kidney Disease</FormLabel>
            <FormSelect
              name="kidney_disease"
              value={formData.kidney_disease}
              onChange={handleInputChange}
            >
              <option value="0">No</option>
              <option value="1">Yes</option>
            </FormSelect>
          </FormGroup>
        </FormGrid>

        {error && <ErrorMessage>{error}</ErrorMessage>}

        <SubmitButton type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Assess Disease Risk'}
        </SubmitButton>
      </form>

      {loading && (
        <LoadingMessage>
          Processing your health data with AI models...
        </LoadingMessage>
      )}
    </FormContainer>
  );
};

export default PredictionForm;
