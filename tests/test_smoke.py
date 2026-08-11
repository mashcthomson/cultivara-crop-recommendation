"""Smoke tests: every regional model + soil label encoder loads cleanly under the
pinned scikit-learn version, and the app's prediction path works end to end on a
sample row built from the shipped data files."""

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
REGIONS = {
    "wheatbelt": "Merredin",
    "kimberley": "Kununurra",
    "southwest": "Manjimup",
}
# Feature order used by app.py:
# [temperature, rainfall, pH, N, P, K, soil_type_encoded]


def load_pair(region):
    from sklearn.exceptions import InconsistentVersionWarning

    with warnings.catch_warnings():
        # Fail hard if the pickles were produced by a different sklearn version.
        # (joblib itself emits an unrelated NumPy 2.5 DeprecationWarning; ignore it.)
        warnings.simplefilter("error", InconsistentVersionWarning)
        model = joblib.load(ROOT / "models" / f"crop_recommendation_{region}.pkl")
        le_soil = joblib.load(ROOT / "models" / f"label_encoder_soil_{region}.pkl")
    return model, le_soil


@pytest.mark.parametrize("region", list(REGIONS))
def test_model_loads_and_predicts(region):
    model, le_soil = load_pair(region)
    assert model.n_features_in_ == 7

    # Build a sample row from the shipped regional data files.
    station = REGIONS[region]
    temp = pd.read_csv(ROOT / "data" / f"Temperature_Data_{station}.csv")
    rain = pd.read_csv(ROOT / "data" / f"Rainfall_Data_{station}.csv")
    soil = pd.read_csv(ROOT / "data" / "Soil_Parameters.csv")
    soil = soil[soil["Region"] == station].iloc[0]

    avg_temp = float(
        (temp["Minimum temperature (°C)"].mean() + temp["Maximum temperature (°C)"].mean()) / 2
    )
    monthly_rain = float(rain["Monthly Rainfall (mm)"].mean())
    soil_encoded = int(le_soil.transform([soil["Soil Type"]])[0])

    features = np.array([[
        avg_temp,
        monthly_rain,
        float(soil["Soil pH"]),
        float(soil["Nitrogen (N%)"]),
        float(soil["Phosphorus (P%)"]),
        float(soil["Potassium (K%)"]),
        soil_encoded,
    ]])
    prediction = model.predict(features)
    crop = prediction[0]
    assert isinstance(crop, str) and crop, f"empty prediction for {region}"
    assert crop in model.classes_
    print(f"{region}: sample features -> {crop} (classes: {list(model.classes_)})")


@pytest.mark.parametrize("region", list(REGIONS))
def test_encoder_covers_app_soil_options(region):
    """Every soil type the app UI offers must be encodable."""
    app_soils = {
        "wheatbelt": ["Sandy Loam", "Clay Loam", "Loamy Sand"],
        "kimberley": ["Clay", "Silt Loam", "Loam"],
        "southwest": ["Loamy Clay", "Sandy Clay", "Clay Loam"],
    }[region]
    _, le_soil = load_pair(region)
    known = set(le_soil.classes_)
    missing = [s for s in app_soils if s not in known]
    assert not missing, f"{region}: UI soil types unknown to encoder: {missing}"


@pytest.mark.parametrize("region", list(REGIONS))
def test_crop_info_json_present(region):
    for suffix in ("cards", "crop_info"):
        path = ROOT / "data" / f"{region}_{suffix}.json"
        with open(path) as f:
            data = json.load(f)
        assert data, f"{path} is empty"
