# Cultivara 🌾 – Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> RMIT University – Master of Data Science Capstone Project

## Overview

Cultivara is a machine learning-powered crop recommendation system designed to help farmers in Western Australia make data-driven decisions about which crops to plant based on soil and climate conditions.

**Achieved 92% classification accuracy** using a Random Forest model trained on regional agricultural data.

## Features

- Crop recommendation based on soil nutrients (N, P, K), temperature, humidity, pH, and rainfall
- Random Forest classifier with hyperparameter tuning
- Interactive Streamlit web application for easy farmer use
- Data preprocessing pipeline with feature engineering
- Model evaluation with confusion matrix and classification report
- Regional coverage across Western Australia zones

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| ML Model | Random Forest (Scikit-learn) |
| Web App | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Serialization | Pickle / Joblib |

## Project Structure

```
cultivara-crop-recommendation/
├── app.py                  # Streamlit web application
├── model/
│   ├── train_model.py      # Model training script
│   ├── crop_model.pkl      # Trained Random Forest model
│   └── evaluate_model.py   # Model evaluation
├── data/
│   ├── crop_data.csv       # Training dataset
│   └── preprocessing.py    # Data cleaning & feature engineering
├── notebooks/
│   ├── EDA.ipynb           # Exploratory Data Analysis
│   └── Model_Training.ipynb
├── requirements.txt
└── README.md
```

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 92% |
| Precision (macro avg) | 0.91 |
| Recall (macro avg) | 0.92 |
| F1-Score (macro avg) | 0.91 |

## Key Learnings

- Hands-on experience with end-to-end ML pipeline development
- Team leadership across 6 members covering data engineering, modeling, and deployment
- Stakeholder testing and iterative feedback loops
- Deploying interactive data apps with Streamlit

## Team

RMIT University – Master of Data Science (2023–2025)  
Team of 6 | Project Lead: Monish Chezhian

---

*Part of RMIT Master of Data Science program, 2024*
