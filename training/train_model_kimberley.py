# train_model_kimberley.py

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import warnings
import datetime

warnings.filterwarnings('ignore')

from pathlib import Path

# Resolve paths relative to the repo root so the script works from any cwd.
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
MODELS = ROOT / 'models'
MODELS.mkdir(exist_ok=True)

region = 'Kimberley'
region_lower = region.lower()

# Load Data
temp_data = pd.read_csv(DATA / 'Temperature_Data_Kununurra.csv')
rainfall_data = pd.read_csv(DATA / 'Rainfall_Data_Kununurra.csv')
soil_data = pd.read_csv(DATA / 'Soil_Parameters.csv')
crop_data = pd.read_csv(DATA / 'Crop_Parameters_Kimberley.csv')
irrigation_data = pd.read_csv(DATA / 'Irrigation_Parameters.csv')

# Filter soil data for Kimberley (Kununurra)
soil_data = soil_data[soil_data['Region'] == 'Kununurra']

# Data Preprocessing
temp_data['Date'] = pd.to_datetime(temp_data['Date'])
rainfall_data['Date'] = pd.to_datetime(rainfall_data['Date'])

# Merge temperature and rainfall data
weather_data = pd.merge(temp_data, rainfall_data, on=['Date', 'Station Name', 'Region Name'])

# Calculate average temperature and total rainfall for each month
weather_data['Month'] = weather_data['Date'].dt.month
monthly_weather = weather_data.groupby('Month').agg({
    'Minimum temperature (°C)': 'mean',
    'Maximum temperature (°C)': 'mean',
    'Daily Rainfall (mm)': 'sum'
}).reset_index()

monthly_weather.rename(columns={
    'Minimum temperature (°C)': 'Avg Min Temp (°C)',
    'Maximum temperature (°C)': 'Avg Max Temp (°C)',
    'Daily Rainfall (mm)': 'Total Rainfall (mm)'
}, inplace=True)

# Prepare the dataset for training
# Merge crop data with soil data
soil_crop_data = pd.merge(crop_data, soil_data, on=['Soil Type'])

# This merge silently drops any crop whose 'Soil Type' in
# Crop_Parameters_Kimberley.csv is not one of this region's soil types in
# Soil_Parameters.csv. That has been happening without any signal, so name it.
dropped_crops = sorted(set(crop_data['Crop']) - set(soil_crop_data['Crop']))
if dropped_crops:
    print(f"WARNING for {region}: these crops have a soil type not found in "
          f"Soil_Parameters.csv for this region and were excluded from "
          f"training, they can never be recommended until the soil type is "
          f"corrected: {dropped_crops}")

# Convert 'Planting Month' to numerical month
soil_crop_data['Planting Month Number'] = pd.to_datetime(soil_crop_data['Planting Month'], format='%B').dt.month

# Merge with monthly weather data based on planting month
full_data = pd.merge(soil_crop_data, monthly_weather, left_on='Planting Month Number', right_on='Month')

# Check the columns of full_data
print("Columns in full_data:", full_data.columns.tolist())

# Features and target
features = ['Optimal Temperature (°C)', 'Total Rainfall (mm)', 'Soil pH',
            'Nitrogen (N%)', 'Phosphorus (P%)', 'Potassium (K%)']
target = 'Crop'

# Encode 'Soil Type'
le_soil = LabelEncoder()
# Fit on the region's full soil-type list (Soil_Parameters.csv), not just the
# soil types that survive the crop/soil merge, so every soil the app offers
# for this region can be encoded at prediction time.
le_soil.fit(soil_data['Soil Type'])
full_data['Soil Type Encoded'] = le_soil.transform(full_data['Soil Type'])
features.append('Soil Type Encoded')

X = full_data[features]
y = full_data[target]

# No held-out split. With one row per crop class in this table, a
# train_test_split does not measure generalization, it deterministically
# removes whichever class lands in the test fold from the trained model's
# classes_ entirely, so that crop could never be recommended again even
# though it belongs to this region. That is a correctness bug, not a modeling
# choice, so this trains on every row the soil merge left it, and reports
# class coverage honestly instead of a held-out accuracy number that cannot
# be meaningful at this sample size.
print(f"Training {region} on {len(X)} rows, {y.nunique()} classes: {sorted(y.unique())}")
print(f"(No held-out accuracy is computed. At roughly one row per class, any "
      f"split would remove a class from training rather than measure it. See "
      f"README.md for the same caveat.)")

# Train the model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save the model
joblib.dump(clf, MODELS / f'crop_recommendation_{region_lower}.pkl')

# Save the label encoder
joblib.dump(le_soil, MODELS / f'label_encoder_soil_{region_lower}.pkl')

print(f"Model and label encoder for {region} saved successfully.")
