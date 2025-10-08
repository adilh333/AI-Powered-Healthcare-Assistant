import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PredictionForm from './components/PredictionForm';
import Results from './components/Results';
import Navigation from './components/Navigation';
import './index.css';

function App() {
  const [predictions, setPredictions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePrediction = (predictionData) => {
    setPredictions(predictionData);
    setError(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setPredictions(null);
  };

  const clearResults = () => {
    setPredictions(null);
    setError(null);
  };

  return (
    <div className="healthcare-dashboard">
      <Navigation />
      <div className="dashboard-header">
        <h1 className="dashboard-title">AI-Powered Healthcare Assistant</h1>
        <p className="dashboard-subtitle">
          Advanced Disease Risk Prediction using Machine Learning
        </p>
      </div>
      
      <div style={{ padding: '0 2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <Routes>
          <Route 
            path="/" 
            element={
              <Dashboard 
                predictions={predictions}
                loading={loading}
                error={error}
                onClear={clearResults}
              />
            } 
          />
          <Route 
            path="/predict" 
            element={
              <PredictionForm 
                onPrediction={handlePrediction}
                onError={handleError}
                onLoading={setLoading}
              />
            } 
          />
          <Route 
            path="/results" 
            element={
              <Results 
                predictions={predictions}
                error={error}
                onClear={clearResults}
              />
            } 
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
