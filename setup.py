#!/usr/bin/env python3
"""
Setup script for Healthcare Assistant
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="healthcare-assistant",
    version="1.0.0",
    author="Healthcare Assistant Team",
    author_email="healthcare.assistant@example.com",
    description="AI-Powered Healthcare Assistant for Early Disease Prediction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/Healthcare_Assistant",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/Healthcare_Assistant/issues",
        "Source": "https://github.com/YOUR_USERNAME/Healthcare_Assistant",
        "Documentation": "https://github.com/YOUR_USERNAME/Healthcare_Assistant#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.6.1",
        ],
        "docs": [
            "sphinx>=7.2.6",
            "sphinx-rtd-theme>=1.3.0",
            "mkdocs>=1.5.3",
            "mkdocs-material>=9.4.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "healthcare-assistant=app:main",
            "train-models=train_models:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "healthcare",
        "machine-learning",
        "disease-prediction",
        "ai",
        "medical",
        "streamlit",
        "flask",
        "xgboost",
        "scikit-learn",
    ],
    zip_safe=False,
)
