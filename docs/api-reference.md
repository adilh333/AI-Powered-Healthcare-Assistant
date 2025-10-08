# API Reference

## Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Check application health

### Model Information
- **URL**: `/models/info`
- **Method**: GET
- **Description**: Get information about loaded models

### Disease Predictions
- **URL**: `/predict/{disease_type}`
- **Method**: POST
- **Description**: Predict disease risk
- **Disease Types**: diabetes, heart_disease, eye_disease

### All Predictions
- **URL**: `/predict/all`
- **Method**: POST
- **Description**: Get predictions for all diseases

## Request/Response Examples

See main README.md for detailed examples.
