# Deployment Guide

## Local Deployment
1. Follow installation guide
2. Run `python run_app.py`
3. Access at http://localhost:8501

## Azure Deployment
1. Install Azure CLI
2. Run `deploy-to-azure.bat`
3. Access deployed app at Azure URL

## Docker Deployment
```bash
docker build -t healthcare-assistant .
docker run -p 8501:8501 healthcare-assistant
```

## Production Considerations
- Use production WSGI server (Gunicorn)
- Configure proper logging
- Set up monitoring and alerts
- Use environment variables for configuration
