# Bike Share Analysis (Washington, D.C.) — EDA & Streamlit Dashboard

A compact, end‑to‑end data analysis of the Capital Bikeshare dataset (2011–2012) featuring a clean Exploratory Data Analysis (EDA) notebook and an interactive Streamlit dashboard. The project answers practical business questions about demand drivers and daily/hourly usage patterns to support operations and product decisions.

## Problem Statements

This project explores three core questions:
- How does perceived temperature (atemp) influence the number of bike users, for both registered and casual segments?
- How do seasons affect total usage?
- What do 24‑hour usage patterns look like on working days vs. weekends/holidays?

## Data

Two related datasets are used:
- `Data/day.csv` — Daily aggregates
- `Data/hour.csv` — Hourly aggregates

The same raw files are duplicated under `Dashboard/` for the app. Key columns include date (`dteday`), season, month, weekday, workingday, weather situation, temperature (normalized), humidity (normalized), windspeed (normalized), and demand targets: `casual`, `registered`, `cnt`.

Data normalization in the original source is reversed in this project for interpretability:
- `temp × 41`, `atemp × 50`, `hum × 100`, `windspeed × 67`

Time coverage: 2011–2012 (Washington, D.C.).

## Methods & Workflow

- Data wrangling
  - Load daily and hourly datasets
  - Restore real‑world scales for temp/atemp/hum/windspeed
  - Parse dates and map categorical codes to labels (month, season, weekday, workingday, weather)
- Data quality
  - Checked info schemas and visualized missingness (none found)
  - Quick outlier scan via boxplots; retained outliers to preserve real demand spikes
- EDA (Notebook)
  - Distributions (histograms), relationships (pairplot, heatmap), time series (daily/hourly lines)
  - Segment comparisons across seasons and user types
- Explanatory visuals & dashboarding
  - Reproducible figures in the notebook and an interactive Streamlit app for lightweight exploration

## Key Insights

- Temperature matters, especially for registered users
  - Both `registered` and `casual` increase with perceived temperature, but the effect is stronger for `registered`.
- Seasonality is clear
  - Peak demand in Summer and Fall; trough in Winter.
- Daily rhythm (hourly)
  - Working days: pronounced rush‑hour peaks (≈06–09 and ≈15–18), dominated by registered users.
  - Weekends/holidays: broader midday‑to‑afternoon peak (≈10–20), relatively more casual usage.
- Distributional notes
  - Overall numeric distributions are reasonable (some right‑skew in casual and windspeed). No missing data.

## What’s in the Repository

```
Proyek_Analisis_Data.ipynb      # EDA & explanatory analysis (Indonesian)
Dashboard/
  dashboard.py                  # Streamlit app
  day.csv, hour.csv             # App copy of datasets
  requirements.txt              # Minimal libs for figures (additions below)
Data/
  day.csv, hour.csv             # Source datasets used in the notebook
```

## Dashboard — Features at a Glance

- KPIs: total, registered, and casual users
- Date‑range filter for daily line charts (choose `registered`, `casual`, `cnt`)
- Temperature vs. users scatter (atemp vs registered/casual)
- Hourly usage for a selected date
- Segment views: pie (casual vs registered) and seasonal bar chart

## How to Run

### 1) Set up a Python environment

```powershell
# From the repository root
python -m venv .venv; .\.venv\Scripts\Activate
python -m pip install --upgrade pip

# Install base requirements (for the dashboard figures)
pip install -r Dashboard\requirements.txt

# Add missing packages used across the project
pip install streamlit missingno
```

### 2) Run the Streamlit dashboard

```powershell
# From the repository root
streamlit run Dashboard\dashboard.py
```

### 3) Open and run the EDA notebook

- File: `Proyek_Analisis_Data.ipynb`
- Ensure Jupyter support is available in your environment. If needed:

```powershell
pip install notebook jupyterlab
```

## Reproduction Notes

- The notebook and dashboard internally denormalize temperature, humidity, and windspeed for readability.
- Categorical fields are mapped to human‑readable labels to simplify plots and filtering.

## Possible Future Work

- Forecasting: build classical or ML models (SARIMAX, Prophet, XGBoost/LGBM) to predict hourly/daily `cnt` by season and weather features.
- Operations optimization: dynamic bike allocation and rebalancing using demand forecasts and spatial data (if station‑level data is available).
- Price/discount experiments: simulate elasticity by segment (registered vs casual) under weather and season scenarios.
- Anomaly detection: identify unusual spikes/drops (events, outages, severe weather) for alerting.
- App hardening: package a consolidated `requirements.txt` (root level), Dockerfile, and CI checks.

## Attribution

- Dataset derived from the Capital Bikeshare system (Washington, D.C.), widely distributed in public ML repositories.

## Maintainer and Creator

- Name: Abdillah Ilham  
- Email: ilhamabdilerz@gmail.com  
