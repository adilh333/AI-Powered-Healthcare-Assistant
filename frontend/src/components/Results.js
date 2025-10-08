import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import styled from 'styled-components';

const ResultsContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

const ResultsHeader = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  text-align: center;
`;

const ResultsTitle = styled.h2`
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 600;
  margin: 0 0 1rem 0;
`;

const ResultsSubtitle = styled.p`
  color: #7f8c8d;
  font-size: 1.1rem;
  margin: 0;
`;

const PredictionGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
`;

const PredictionCard = styled.div`
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  }
`;

const CardHeader = styled.div`
  background: ${props => {
    if (props.riskLevel === 'High') return 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)';
    if (props.riskLevel === 'Medium') return 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)';
    return 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
  }};
  color: white;
  padding: 1.5rem;
  text-align: center;
`;

const CardTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
`;

const CardSubtitle = styled.p`
  font-size: 1rem;
  margin: 0;
  opacity: 0.9;
`;

const CardContent = styled.div`
  padding: 2rem;
`;

const RiskScore = styled.div`
  font-size: 3rem;
  font-weight: 700;
  text-align: center;
  margin: 1rem 0;
  color: ${props => {
    if (props.riskLevel === 'High') return '#e74c3c';
    if (props.riskLevel === 'Medium') return '#f39c12';
    return '#27ae60';
  }};
`;

const RiskLevel = styled.div`
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: ${props => {
    if (props.riskLevel === 'High') return '#e74c3c';
    if (props.riskLevel === 'Medium') return '#f39c12';
    return '#27ae60';
  }};
`;

const Recommendations = styled.div`
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1.5rem;
`;

const RecommendationsTitle = styled.h4`
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1.2rem;
`;

const RecommendationsList = styled.ul`
  margin: 0;
  padding-left: 1.5rem;
  color: #555;
`;

const RecommendationItem = styled.li`
  margin-bottom: 0.5rem;
  line-height: 1.5;
`;

const ChartsSection = styled.div`
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const ChartsTitle = styled.h3`
  color: #2c3e50;
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0 0 2rem 0;
  text-align: center;
`;

const ChartsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
`;

const ChartContainer = styled.div`
  height: 300px;
`;

const ErrorMessage = styled.div`
  background: #fee;
  color: #c33;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #fcc;
`;

const NoResultsMessage = styled.div`
  background: white;
  border-radius: 12px;
  padding: 3rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #7f8c8d;
  font-size: 1.1rem;
`;

const ClearButton = styled.button`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-top: 1rem;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
`;

const Results = ({ predictions, error, onClear }) => {
  if (error) {
    return (
      <ResultsContainer>
        <ErrorMessage>
          <h3>Error</h3>
          <p>{error}</p>
          <ClearButton onClick={onClear}>Try Again</ClearButton>
        </ErrorMessage>
      </ResultsContainer>
    );
  }

  if (!predictions) {
    return (
      <ResultsContainer>
        <NoResultsMessage>
          <h3>No Results Available</h3>
          <p>Please complete a health risk assessment to view results.</p>
        </NoResultsMessage>
      </ResultsContainer>
    );
  }

  const diseaseNames = {
    diabetes: 'Diabetes',
    heart_disease: 'Heart Disease',
    eye_disease: 'Eye Disease'
  };

  const riskColors = {
    Low: '#27ae60',
    Medium: '#f39c12',
    High: '#e74c3c'
  };

  // Prepare data for charts
  const pieData = Object.entries(predictions.predictions).map(([disease, prediction]) => ({
    name: diseaseNames[disease] || disease,
    value: prediction.risk_score * 100,
    riskLevel: prediction.risk_level,
    color: riskColors[prediction.risk_level]
  }));

  const barData = Object.entries(predictions.predictions).map(([disease, prediction]) => ({
    disease: diseaseNames[disease] || disease,
    riskScore: prediction.risk_score * 100,
    riskLevel: prediction.risk_level
  }));

  return (
    <ResultsContainer>
      <ResultsHeader>
        <ResultsTitle>Health Risk Assessment Results</ResultsTitle>
        <ResultsSubtitle>
          Analysis completed on {new Date(predictions.timestamp).toLocaleString()}
        </ResultsSubtitle>
        <ClearButton onClick={onClear}>New Assessment</ClearButton>
      </ResultsHeader>

      <PredictionGrid>
        {Object.entries(predictions.predictions).map(([disease, prediction]) => (
          <PredictionCard key={disease}>
            <CardHeader riskLevel={prediction.risk_level}>
              <CardTitle>{diseaseNames[disease] || disease}</CardTitle>
              <CardSubtitle>Risk Assessment</CardSubtitle>
            </CardHeader>
            <CardContent>
              <RiskScore riskLevel={prediction.risk_level}>
                {(prediction.risk_score * 100).toFixed(1)}%
              </RiskScore>
              <RiskLevel riskLevel={prediction.risk_level}>
                {prediction.risk_level} Risk
              </RiskLevel>
              
              <Recommendations>
                <RecommendationsTitle>Recommendations</RecommendationsTitle>
                <RecommendationsList>
                  {prediction.recommendations.map((rec, index) => (
                    <RecommendationItem key={index}>{rec}</RecommendationItem>
                  ))}
                </RecommendationsList>
              </Recommendations>
            </CardContent>
          </PredictionCard>
        ))}
      </PredictionGrid>

      <ChartsSection>
        <ChartsTitle>Risk Score Visualization</ChartsTitle>
        <ChartsGrid>
          <ChartContainer>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
              </PieChart>
            </ResponsiveContainer>
          </ChartContainer>

          <ChartContainer>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="disease" />
                <YAxis />
                <Tooltip formatter={(value) => `${value.toFixed(1)}%`} />
                <Bar 
                  dataKey="riskScore" 
                  fill="#667eea"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartContainer>
        </ChartsGrid>
      </ChartsSection>
    </ResultsContainer>
  );
};

export default Results;
