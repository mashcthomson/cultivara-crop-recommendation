"""
Shared training pipeline for the three regional models.

Each train_model_<region>.py script just points this at its regional CSV.
Keeps the per-region scripts short and guarantees all three models are
trained and evaluated the same way.
"""

import os

import joblib
import matplotlib

matplotlib.use("Agg")  # no display needed when training from the terminal
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder

FEATURE_COLUMNS = ["N%", "P%", "K%", "temperature", "humidity", "ph", "rainfall"]

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(HERE, "models")


def train_regional_model(region, csv_path, random_state=42):
    """Train, evaluate and save the Random Forest model for one region."""
    print(f"=== Training model: {region} ===")

    full_data = pd.read_csv(csv_path)
    print(f"Loaded {len(full_data)} rows, {full_data['label'].nunique()} crops "
          f"({', '.join(sorted(full_data['label'].unique()))})")

    X = full_data[FEATURE_COLUMNS]

    encoder = LabelEncoder()
    y = encoder.fit_transform(full_data["label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state
    )

    # Light hyperparameter search — RF barely needs it on this data, but it
    # keeps the model size sensible and the choice honest.
    param_grid = {
        "n_estimators": [100, 150],
        "max_depth": [10, 15],
        "min_samples_leaf": [1, 2],
    }
    search = GridSearchCV(
        RandomForestClassifier(random_state=random_state),
        param_grid,
        cv=5,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    model = search.best_estimator_
    print(f"Best params: {search.best_params_} (CV accuracy {search.best_score_:.4f})")

    # --- Evaluation on the held-out test set ---
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="macro", zero_division=0
    )

    print(f"\nTest accuracy:          {accuracy:.4f}")
    print(f"Macro precision:        {precision:.4f}")
    print(f"Macro recall:           {recall:.4f}")
    print(f"Macro F1:               {f1:.4f}\n")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_,
                                zero_division=0))

    os.makedirs(MODELS_DIR, exist_ok=True)

    # Confusion matrix plot
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=encoder.classes_, yticklabels=encoder.classes_)
    plt.title(f"Confusion matrix – {region}")
    plt.xlabel("Predicted crop")
    plt.ylabel("Actual crop")
    plt.tight_layout()
    cm_path = os.path.join(MODELS_DIR, f"confusion_matrix_{region}.png")
    plt.savefig(cm_path, dpi=120)
    plt.close()
    print(f"Saved confusion matrix -> {cm_path}")

    # Persist everything the app needs in one bundle
    bundle = {
        "model": model,
        "encoder": encoder,
        "features": FEATURE_COLUMNS,
    }
    model_path = os.path.join(MODELS_DIR, f"crop_model_{region}.joblib")
    joblib.dump(bundle, model_path, compress=3)
    size_mb = os.path.getsize(model_path) / 1e6
    print(f"Saved model -> {model_path} ({size_mb:.2f} MB)")

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}
