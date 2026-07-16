"""Train the South West regional model (temperate mediterranean horticulture)."""

import os

from training_utils import train_regional_model

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "..", "data", "southwest.csv")

if __name__ == "__main__":
    train_regional_model("southwest", CSV_PATH)
