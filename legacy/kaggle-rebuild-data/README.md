# Data

## Where this data comes from

The original regional datasets we compiled for the capstone (pulled together
from WA agricultural sources during the project) were not recoverable — they
lived on the uni project drive, which is long gone. To keep the three-region
design intact, the training data here is reconstructed from the public
[Kaggle Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
(2,200 rows, 22 crops, 100 rows per crop).

`make_regional_datasets.py` splits the master file (`crop_data.csv`) into
three climate-analog regional subsets, matching each crop's actual
temperature/rainfall distribution in the data against the climate of the
three WA regions the project targeted:

| Region | Climate | Crops |
|--------|---------|-------|
| **Kimberley** | Tropical monsoonal north — hot, high rainfall (95–236 mm in-data) | rice, banana, coconut, papaya, mango, jute, coffee, pigeonpeas |
| **Wheatbelt** | Semi-arid grain/pulse country — low rainfall dryland (46–106 mm) | chickpea, lentil, mothbeans, mungbean, blackgram, kidneybeans, cotton, maize |
| **South West** | Temperate mediterranean — mild-climate horticulture | apple, grapes, orange, pomegranate, watermelon, muskmelon, maize |

Maize appears in both Wheatbelt and South West on purpose — its climate
envelope (mild temperatures, ~85 mm rainfall) genuinely spans both regions,
and it's grown in both in practice.

## Columns

Nutrient columns are renamed `N` / `P` / `K` → `N%` / `P%` / `K%` during
preprocessing (the convention the app and models use throughout).

| Column | Meaning |
|--------|---------|
| `N%`, `P%`, `K%` | Soil nitrogen / phosphorus / potassium content |
| `temperature` | Temperature (°C) |
| `humidity` | Relative humidity (%) |
| `ph` | Soil pH |
| `rainfall` | Rainfall (mm) |
| `label` | Crop (target) |

## Regenerating the regional files

```bash
python make_regional_datasets.py
```

Produces `kimberley.csv`, `wheatbelt.csv`, `southwest.csv` alongside the
master file.
