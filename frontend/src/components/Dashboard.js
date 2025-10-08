import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

const DashboardContainer = styled.div`
  display: grid;
  gap: 2rem;
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const StatCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const StatValue = styled.div`
  font-size: 3rem;
  font-weight: 700;
  color: #667eea;
  margin: 0;
`;

const StatLabel = styled.div`
  color: #7f8c8d;
  font-size: 1rem;
  margin: 0.5rem 0 0 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

const FeatureGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
`;

const FeatureCard = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
  }
`;

const FeatureTitle = styled.h3`
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
`;

const FeatureDescription = styled.p`
  color: #7f8c8d;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
`;

const FeatureList = styled.ul`
  color: #555;
  margin: 0;
  padding-left: 1.5rem;
`;

const FeatureItem = styled.li`
  margin-bottom: 0.5rem;
`;

const CTAButton = styled(Link)`
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 100%;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
`;

const ResultsSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
`;

const ResultsTitle = styled.h2`
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0 0 1.5rem 0;
  text-align: center;
`;

const NoResults = styled.div`
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
  padding: 2rem;
`;

const Dashboard = ({ predictions, loading, error, onClear }) => {
  return (
    <DashboardContainer>
      <StatsGrid>
        <StatCard>
          <StatValue>3</StatValue>
          <StatLabel>Disease Types</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>95%</StatValue>
          <StatLabel>Accuracy</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>ML</StatValue>
          <StatLabel>AI Models</StatLabel>
        </StatCard>
        <StatCard>
          <StatValue>24/7</StatValue>
          <StatLabel>Available</StatLabel>
        </StatCard>
      </StatsGrid>

      <FeatureGrid>
        <FeatureCard>
          <FeatureTitle>Diabetes Prediction</FeatureTitle>
          <FeatureDescription>
            Advanced machine learning models analyze your health data to predict diabetes risk with high accuracy.
          </FeatureDescription>
          <FeatureList>
            <FeatureItem>Blood glucose analysis</FeatureItem>
            <FeatureItem>BMI and lifestyle factors</FeatureItem>
            <FeatureItem>Family history consideration</FeatureItem>
            <FeatureItem>Personalized recommendations</FeatureItem>
          </FeatureList>
        </FeatureCard>

        <FeatureCard>
          <FeatureTitle>Heart Disease Risk</FeatureTitle>
          <FeatureDescription>
            Comprehensive cardiovascular risk assessment using multiple health indicators and lifestyle factors.
          </FeatureDescription>
          <FeatureList>
            <FeatureItem>Cholesterol and blood pressure</FeatureItem>
            <FeatureItem>Exercise and diet analysis</FeatureItem>
            <FeatureItem>Smoking and alcohol factors</FeatureItem>
            <FeatureItem>Early intervention guidance</FeatureItem>
          </FeatureList>
        </FeatureCard>

        <FeatureCard>
          <FeatureTitle>Eye Disease Detection</FeatureTitle>
          <FeatureDescription>
            Predictive analysis for eye diseases including diabetic retinopathy and age-related conditions.
          </FeatureDescription>
          <FeatureList>
            <FeatureItem>Diabetes correlation analysis</FeatureItem>
            <FeatureItem>Age and hypertension factors</FeatureItem>
            <FeatureItem>Family history assessment</FeatureItem>
            <FeatureItem>Preventive care recommendations</FeatureItem>
          </FeatureList>
        </FeatureCard>
      </FeatureGrid>

      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <CTAButton to="/predict">
          Start Risk Assessment
        </CTAButton>
      </div>

      {(predictions || error) && (
        <ResultsSection>
          <ResultsTitle>Latest Assessment Results</ResultsTitle>
          {error && (
            <div style={{ 
              background: '#fee', 
              color: '#c33', 
              padding: '1rem', 
              borderRadius: '8px',
              marginBottom: '1rem',
              border: '1px solid #fcc'
            }}>
              Error: {error}
            </div>
          )}
          {predictions && (
            <div>
              <p style={{ textAlign: 'center', color: '#7f8c8d', marginBottom: '1rem' }}>
                Assessment completed successfully. View detailed results below.
              </p>
              <div style={{ textAlign: 'center' }}>
                <CTAButton to="/results">
                  View Detailed Results
                </CTAButton>
              </div>
            </div>
          )}
        </ResultsSection>
      )}
    </DashboardContainer>
  );
};

export default Dashboard;
