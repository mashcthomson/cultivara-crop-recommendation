# Cultivara 🌾 – Crop Recommendation System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

> RMIT University – Master of Data Science Capstone Project

---

## What this is

Cultivara started as a uni project but turned into something I genuinely cared about finishing properly.

The idea: farmers in Western Australia have to make crop decisions based on soil composition, rainfall, temperature, and humidity — often relying on experience and gut feel. We built a system that takes those inputs and tells you what to plant, backed by Random Forest models trained on regional agricultural data.

The key design decision was **one model per region, not one model for all of WA**. The Kimberley, the Wheatbelt, and the South West are basically three different climates that happen to share a state border, and a single combined model kept confusing crops across those zones. Splitting into three regional models made each one's job much easier — and it means a Wheatbelt farmer never gets told to plant coconuts.

More importantly, we shipped a working Streamlit app that a non-technical farmer could actually open and use without needing to understand what a model is.

I led a team of 6 through the whole thing — from the messy early data wrangling stages through to stakeholder testing and the final presentation. Good experience in keeping a project moving when everyone has different ideas about what done means.

---

## What it does

- Takes soil nutrient levels (N%, P%, K%), temperature, humidity, pH, and rainfall as input
- You pick your region — **Wheatbelt**, **Kimberley**, or **South West** — and the app runs the inputs through that region's tuned Random Forest classifier
- Returns the most suitable crop plus the top-3 options with confidence scores
- Displays results through a clean Streamlit interface built for farmers, not data scientists

---

## A note on the data

The original regional datasets we compiled during the capstone were on the uni project drive and weren't recoverable when I rebuilt this repo. To keep the three-region architecture intact, the training data here is reconstructed from the public [Kaggle Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset) (2,200 rows, 22 crops), partitioned into three climate-analog regional subsets by matching each crop's actual temperature/rainfall envelope against the climate of the three WA regions:

- **Kimberley** — tropical monsoonal north: rice, banana, coconut, papaya, mango, jute, coffee, pigeonpeas
- **Wheatbelt** — semi-arid grain and pulse country: chickpea, lentil, mothbeans, mungbean, blackgram, kidneybeans, cotton, maize
- **South West** — temperate mediterranean horticulture: apple, grapes, orange, pomegranate, watermelon, muskmelon, maize

(Maize sits in both Wheatbelt and South West deliberately — its climate envelope genuinely spans both.) Full details and the split script are in [`data/`](data/README.md).

---

## Model performance

Measured on a held-out, stratified 20% test set per region (fixed random seed, full training logs reproducible via the train scripts):

| Region | Test accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|--------|--------------|-------------------|----------------|------------|
| Wheatbelt | 99.4% | 0.994 | 0.994 | 0.994 |
| Kimberley | 98.1% | 0.982 | 0.981 | 0.981 |
| South West | 100% | 1.000 | 1.000 | 1.000 |

Each training script also produces a full per-crop classification report and a confusion matrix PNG (in `crop_recommender_app/Ver 4 - Streamlit/models/`). Worth being upfront: the Kaggle dataset is cleaner and more separable than real paddock data, so these numbers are a ceiling, not a promise. The only confusions the models make are the sensible ones (rice vs jute in the Kimberley — similar heat and rainfall; lentil vs mothbeans in the Wheatbelt).

---

## Tech stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.9+ |
| ML Model | Random Forest (Scikit-learn), tuned with GridSearchCV |
| Web App | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Serialization | Joblib |

---

## Project structure

```
cultivara-crop-recommendation/
├── crop_recommender_app/
│   ├── Ver 3 - Streamlit/            # Earlier iteration: one combined model
│   │   ├── train_model.py
│   │   ├── app.py
│   │   └── model/crop_model.joblib
│   └── Ver 4 - Streamlit/            # Final version: three regional models
│       ├── train_model_wheatbelt.py
│       ├── train_model_kimberley.py
│       ├── train_model_southwest.py
│       ├── training_utils.py         # Shared training/eval pipeline
│       ├── app.py                    # Streamlit app with region selector
│       └── models/                   # Trained models + confusion matrices
├── data/
│   ├── crop_data.csv                 # Master dataset (Kaggle)
│   ├── make_regional_datasets.py     # Builds the 3 regional CSVs
│   ├── wheatbelt.csv
│   ├── kimberley.csv
│   ├── southwest.csv
│   └── README.md                     # Data provenance + region assignments
├── requirements.txt
└── README.md
```

Ver 3 is kept in the repo because the jump from one combined model to three regional ones was the most important decision in the project, and I like being able to point at the before and after.

---

## Running it locally

```bash
git clone https://github.com/mashcthomson/cultivara-crop-recommendation.git
cd cultivara-crop-recommendation
pip install -r requirements.txt
cd "crop_recommender_app/Ver 4 - Streamlit"
streamlit run app.py
```

Trained models are included, so the app works straight after cloning. To retrain from scratch:

```bash
cd data && python make_regional_datasets.py && cd "../crop_recommender_app/Ver 4 - Streamlit"
python train_model_wheatbelt.py
python train_model_kimberley.py
python train_model_southwest.py
```

---

## What I took away from this

Leading a team of six through a full ML project taught me things that no amount of solo coding does. Keeping everyone aligned when you're dealing with data cleaning disagreements, model tuning debates, and a hard deadline is genuinely hard.

Technically: end-to-end pipeline work, hyperparameter tuning, deploying an ML app that non-technical people can actually use. And the big modelling lesson — sometimes the best accuracy gain isn't a fancier model, it's splitting the problem along a boundary the domain already gives you.

Practically: how to run a project when you're also the one doing the work.

---

*RMIT University – Master of Data Science, 2024*
