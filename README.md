# Cultivara 🌾 – Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> RMIT University – Master of Data Science Capstone Project

---

## What this is

Cultivara started as a uni project but turned into something I genuinely cared about finishing properly.

The idea: farmers in Western Australia have to make crop decisions based on soil composition, rainfall, temperature, and humidity — often relying on experience and gut feel. We built a system that takes those inputs and tells you what to plant, backed by a Random Forest model trained on regional agricultural data.

We hit **92% classification accuracy** across the crop categories. More importantly, we shipped a working Streamlit app that a non-technical farmer could actually open and use without needing to understand what a model is.

I led a team of 6 through the whole thing — from the messy early data wrangling stages through to stakeholder testing and the final presentation. Good experience in keeping a project moving when everyone has different ideas about what done means.

---

## What it does

- Takes soil nutrient levels (N, P, K), temperature, humidity, pH, and rainfall as input
- Runs them through a tuned Random Forest classifier
- Returns the most suitable crop for those conditions
- Displays results through a clean Streamlit interface built for farmers, not data scientists
- Covers multiple regional zones across Western Australia

---

## Model performance

| Metric | Score |
|--------|-------|
| Accuracy | 92% |
| Precision (macro avg) | 0.91 |
| Recall (macro avg) | 0.92 |
| F1-Score (macro avg) | 0.91 |

Evaluated with confusion matrix and full classification report across all crop classes.

---

## Tech stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| ML Model | Random Forest (Scikit-learn) |
| Web App | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Serialization | Pickle / Joblib |

---

## Project structure

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

---

## Running it locally

```bash
git clone https://github.com/mashcthomson/cultivara-crop-recommendation.git
cd cultivara-crop-recommendation
pip install -r requirements.txt
streamlit run app.py
```

---

## What I took away from this

Leading a team of six through a full ML project taught me things that no amount of solo coding does. Keeping everyone aligned when you're dealing with data cleaning disagreements, model tuning debates, and a hard deadline is genuinely hard. 

Technically: end-to-end pipeline work, hyperparameter tuning, deploying an ML app that non-technical people can actually use. Practically: how to run a project when you're also the one doing the work.

---

*RMIT University – Master of Data Science, 2024*
