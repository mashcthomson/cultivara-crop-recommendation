"""
Cultivara – Ver 3 app. One combined model over all crops, no region
selection yet. Superseded by Ver 4 (three regional models).

Run:  streamlit run app.py
"""

import os

import joblib
import pandas as pd
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))


@st.cache_resource
def load_bundle():
    return joblib.load(os.path.join(HERE, "model", "crop_model.joblib"))


st.title("🌾 Cultivara (Ver 3)")
st.write("Enter your soil and climate values to get a crop recommendation.")

n = st.number_input("Nitrogen (N%)", 0.0, 150.0, 50.0)
p = st.number_input("Phosphorus (P%)", 0.0, 150.0, 50.0)
k = st.number_input("Potassium (K%)", 0.0, 210.0, 50.0)
temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.number_input("Humidity (%)", 0.0, 100.0, 70.0)
ph = st.number_input("Soil pH", 3.0, 10.0, 6.5)
rainfall = st.number_input("Rainfall (mm)", 0.0, 300.0, 100.0)

if st.button("Recommend a crop"):
    bundle = load_bundle()
    row = pd.DataFrame(
        [[n, p, k, temperature, humidity, ph, rainfall]],
        columns=bundle["features"],
    )
    pred = bundle["model"].predict(row)[0]
    crop = bundle["encoder"].classes_[pred]
    st.success(f"Recommended crop: **{crop.title()}**")
