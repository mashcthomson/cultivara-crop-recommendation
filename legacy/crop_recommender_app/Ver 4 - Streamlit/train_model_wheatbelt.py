"""Train the Wheatbelt regional model (semi-arid grain and pulse country)."""

import os

from training_utils import train_regional_model

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "..", "data", "wheatbelt.csv")

if __name__ == "__main__":
    train_regional_model("wheatbelt", CSV_PATH)
