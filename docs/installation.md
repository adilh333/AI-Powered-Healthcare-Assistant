# Installation Guide

## Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- Git (for cloning)

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/Healthcare_Assistant.git
cd Healthcare_Assistant
```

### 2. Create Virtual Environment
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n healthcare-assistant python=3.11
conda activate healthcare-assistant
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models
```bash
python train_models.py
```

### 5. Start Application
```bash
python run_app.py
```

## Troubleshooting

### Common Issues
1. **Port already in use**: Change ports in configuration
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Model loading errors**: Ensure models are trained first
