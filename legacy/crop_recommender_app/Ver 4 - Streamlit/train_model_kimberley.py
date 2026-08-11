"""Train the Kimberley regional model (tropical monsoonal north)."""

import os

from training_utils import train_regional_model

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "..", "data", "kimberley.csv")

if __name__ == "__main__":
    train_regional_model("kimberley", CSV_PATH)
