"""
Cultivara – crop recommendation app (Ver 4).

Pick your region, punch in your soil test numbers and local conditions,
and get a crop recommendation from that region's model.

Run:  streamlit run app.py
"""

import os

import joblib
import pandas as pd
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(HERE, "models")

REGIONS = {
    "Wheatbelt": "wheatbelt",
    "Kimberley": "kimberley",
    "South West": "southwest",
}

REGION_BLURB = {
    "Wheatbelt": "Semi-arid grain and pulse country — dryland cropping.",
    "Kimberley": "Tropical monsoonal north — hot, wet-season driven.",
    "South West": "Temperate mediterranean — orchards, vines and melons.",
}


@st.cache_resource
def load_bundle(region_key):
    path = os.path.join(MODELS_DIR, f"crop_model_{region_key}.joblib")
    return joblib.load(path)


st.set_page_config(page_title="Cultivara", page_icon="🌾")

st.title("🌾 Cultivara")
st.write(
    "Enter your soil test results and local conditions, and Cultivara will "
    "recommend the most suitable crop for your region."
)

region = st.selectbox("Your region", list(REGIONS.keys()))
st.caption(REGION_BLURB[region])

st.subheader("Soil nutrients")
col1, col2, col3 = st.columns(3)
with col1:
    n = st.number_input("Nitrogen (N%)", min_value=0.0, max_value=150.0, value=50.0)
with col2:
    p = st.number_input("Phosphorus (P%)", min_value=0.0, max_value=150.0, value=50.0)
with col3:
    k = st.number_input("Potassium (K%)", min_value=0.0, max_value=210.0, value=50.0)

st.subheader("Conditions")
col4, col5 = st.columns(2)
with col4:
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
    ph = st.number_input("Soil pH", min_value=3.0, max_value=10.0, value=6.5)
with col5:
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=300.0, value=100.0)

if st.button("Recommend a crop", type="primary"):
    bundle = load_bundle(REGIONS[region])
    model = bundle["model"]
    encoder = bundle["encoder"]
    features = bundle["features"]

    row = pd.DataFrame(
        [[n, p, k, temperature, humidity, ph, rainfall]], columns=features
    )

    probs = model.predict_proba(row)[0]
    ranked = probs.argsort()[::-1]

    best_crop = encoder.classes_[ranked[0]]
    st.success(f"Recommended crop for the {region}: **{best_crop.title()}**")

    st.write("Top 3 options for these conditions:")
    top3 = pd.DataFrame({
        "Crop": [encoder.classes_[i].title() for i in ranked[:3]],
        "Confidence": [f"{probs[i]:.0%}" for i in ranked[:3]],
    })
    st.table(top3)

    if probs[ranked[0]] < 0.5:
        st.info(
            "The model isn't very confident here — your conditions may sit "
            "between crops, or outside what's typical for this region. "
            "Worth checking the other options above."
        )

st.divider()
st.caption(
    "Cultivara – RMIT Master of Data Science capstone. Recommendations are "
    "a guide only; always cross-check with local agronomy advice."
)
