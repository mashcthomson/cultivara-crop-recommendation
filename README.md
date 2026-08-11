# Cultivara — Cultivating with Climate

A crop recommendation tool for Western Australian farmers. Pick your region, enter your
farm details (date, soil type, and optionally temperature, rainfall, pH and N/P/K levels),
and Cultivara recommends the most suitable crop — along with irrigation, farming-method
and planting-window guidance for it.

An RMIT WIL Group 27 project.

## Regions covered

Each region has its own Random Forest classifier, trained on that region's climate and
soil data. One model per region, because the Kimberley, the Wheatbelt and the South West
are effectively three different climates:

| Region | Reference station | Example crops |
|---|---|---|
| Wheatbelt | Merredin | Wheat, Chickpeas, Sunflower |
| Kimberley | Kununurra | Mango, Papaya, Sugar cane |
| South West | Manjimup | Carrots, Broccoli, Lettuce, Pears |

## How to run

Requires Python 3.11+ (developed and tested on 3.14).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501.

## How to retrain the models

The training scripts live in `training/` and read from `data/`, writing the model and
soil label encoder for their region into `models/`:

```bash
python training/train_model_wheatbelt.py
python training/train_model_kimberley.py
python training/train_model_southwest.py
```

Each script merges the region's crop parameters (`data/Crop_Parameters_<Region>.csv`)
with soil parameters (`data/Soil_Parameters.csv`) and monthly climate aggregates built
from the daily temperature/rainfall series, then fits a `RandomForestClassifier` on
7 features: optimal temperature, total monthly rainfall, soil pH, N%, P%, K%, and an
encoded soil type.

The crop/soil parameter tables are small, roughly one row per crop per region, so
these models train on the full table with no held-out test split. A split would not
measure generalisation at this size, it would just remove whichever crop landed in
the test fold from the trained model's class list entirely. They are effectively
lookup-style classifiers over the regional crop envelopes, not a claim of generalised
prediction, and no accuracy number is reported because none would be meaningful here.

Known gap: a few named crops in each region's `Crop_Parameters_<Region>.csv` are
assigned a soil type that does not appear in that region's rows of
`Soil_Parameters.csv` (for example Wheatbelt's Barley and Lentils are both listed
against "Loam", which is not one of Merredin's three soil types in
`Soil_Parameters.csv`). Those crops are excluded from training and can never be
recommended, even though they still appear as cards on the main page. The training
scripts now print a warning naming the affected crops per region; fixing it requires
someone who knows the correct soil type for each crop to correct the source CSV, so
it has not been guessed or silently changed here.

## Data sources

- Daily climate series (temperature, rainfall, solar exposure, wind, humidity/pressure)
  derived from Bureau of Meteorology (BOM) station observations for Merredin (Wheatbelt),
  Kununurra (Kimberley) and Manjimup (South West), plus synthetic extensions built from
  those observations (`data/DAta.zip` holds the original packaged set; raw BOM extracts
  are under `data/Kununurra/` and `data/Merredin/`).
- Crop, soil and irrigation parameter tables (`data/Crop_Parameters_*.csv`,
  `data/Soil_Parameters.csv`, `data/Irrigation_Parameters.csv`) compiled by the project
  team for the three regions.
- Crop cards and per-crop guidance shown in the app: `data/<region>_cards.json` and
  `data/<region>_crop_info.json`.

## Repository layout

```
app.py           Streamlit app (canonical "Ver 4" build)
data_loader.py   JSON/message loading helpers
data/            Climate CSVs, parameter tables, crop cards/info JSON
models/          Trained models + soil label encoders (joblib .pkl)
training/        Per-region training scripts
static/          CSS, crop images, rotating UI messages
images/          Region banner and crop images
tests/           Smoke tests (pytest tests/test_smoke.py)
legacy/          Superseded earlier versions (Ver 3, a Kaggle-based rebuild,
                 Flask-era templates, and the original sklearn-1.5.2 model pickles)
media/           Presentation media (gitignored, not part of the app)
```

## Credits

RMIT WIL Group 27 project.
