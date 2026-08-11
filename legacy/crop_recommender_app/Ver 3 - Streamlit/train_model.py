"""
Ver 3 training script — the single combined model, before we split the
system into three regional models (see Ver 4). Kept for reference.

Trains one Random Forest over all 22 crops in the master dataset.
"""

import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "..", "data", "crop_data.csv")

FEATURE_COLUMNS = ["N%", "P%", "K%", "temperature", "humidity", "ph", "rainfall"]

full_data = pd.read_csv(CSV_PATH)
full_data = full_data.rename(columns={"N": "N%", "P": "P%", "K": "K%"})

X = full_data[FEATURE_COLUMNS]
encoder = LabelEncoder()
y = encoder.fit_transform(full_data["label"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Test accuracy: {accuracy_score(y_test, y_pred):.4f}\n")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))

out_dir = os.path.join(HERE, "model")
os.makedirs(out_dir, exist_ok=True)
bundle = {"model": model, "encoder": encoder, "features": FEATURE_COLUMNS}
out_path = os.path.join(out_dir, "crop_model.joblib")
joblib.dump(bundle, out_path, compress=3)
print(f"Saved model -> {out_path} ({os.path.getsize(out_path) / 1e6:.2f} MB)")
