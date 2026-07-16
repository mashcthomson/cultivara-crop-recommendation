"""
Builds the three regional training datasets from the master crop dataset.

Background: the original regional datasets we compiled for the capstone
(from WA agricultural sources) were lost with the uni project drive, so
this script reconstructs the three-region design from the public Kaggle
Crop Recommendation Dataset (data/crop_data.csv). Each crop is assigned
to the WA region whose climate best matches that crop's temperature and
rainfall envelope in the data:

  - Kimberley   -> tropical monsoonal north: hot, high rainfall crops
  - Wheatbelt   -> semi-arid grain and pulse country: low rainfall crops
  - South West  -> temperate mediterranean: mild-climate horticulture

Maize appears in both Wheatbelt and South West because its climate
envelope (mild temps, ~85mm rainfall) genuinely spans both regions.

Run:  python make_regional_datasets.py
"""

import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

# Crop -> region assignments, based on each crop's temperature/rainfall
# distribution in the master dataset (see data/README.md for the numbers).
REGION_CROPS = {
    "kimberley": [
        "rice", "banana", "coconut", "papaya",
        "mango", "jute", "coffee", "pigeonpeas",
    ],
    "wheatbelt": [
        "chickpea", "lentil", "mothbeans", "mungbean",
        "blackgram", "kidneybeans", "cotton", "maize",
    ],
    "southwest": [
        "apple", "grapes", "orange", "pomegranate",
        "watermelon", "muskmelon", "maize",
    ],
}


def main():
    master = pd.read_csv(os.path.join(HERE, "crop_data.csv"))

    # Rename nutrient columns to the percent convention used in the app
    master = master.rename(columns={"N": "N%", "P": "P%", "K": "K%"})

    for region, crops in REGION_CROPS.items():
        subset = master[master["label"].isin(crops)].reset_index(drop=True)
        out_path = os.path.join(HERE, f"{region}.csv")
        subset.to_csv(out_path, index=False)
        print(f"{region}: {len(subset)} rows, {subset['label'].nunique()} crops -> {out_path}")


if __name__ == "__main__":
    main()
