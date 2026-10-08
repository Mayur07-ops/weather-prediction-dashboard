# 🌦️ Weather Prediction Pipeline Dashboard

An interactive, pipeline-style weather analysis dashboard built from 366 days of historical weather data (`weather.csv`).  
The **ML pipeline is written in Python**. The **frontend** is pure HTML + CSS + vanilla JS (ECharts).

## 🔴 Live Demo

> Host on GitHub Pages by enabling **Settings → Pages → Deploy from branch → main / root**.  
> Your dashboard will be live at `https://<your-username>.github.io/<repo-name>/weather-dashboard/`

---

## 📁 Project Structure

```
weather-dashboard/
├── index.html              ← Frontend entry point
├── css/
│   └── styles.css          ← Dark theme, pipeline layout, chart cards
├── js/
│   ├── weatherData.js      ← Static data constants (update from EDA output)
│   └── charts.js           ← 7 ECharts chart initialisers
├── python/
│   ├── data.py             ← CSV loader & preprocessor (pandas)
│   ├── eda.py              ← Exploratory Data Analysis — computes all chart stats
│   ├── model.py            ← Rule-based rain prediction model + evaluation metrics
│   └── requirements.txt    ← Python dependencies
└── README.md
```

---

## 🐍 Python Pipeline

### Install dependencies

```bash
pip install -r weather-dashboard/python/requirements.txt
```

### Step 1 — Load & preprocess data

```bash
python weather-dashboard/python/data.py
```
Loads `weather.csv`, imputes NA values with column medians, encodes rain flags as booleans.

### Step 2 — Run EDA

```bash
python weather-dashboard/python/eda.py --csv weather.csv
```
Prints a JSON summary with monthly stats, temperature/humidity/cloud distributions, wind direction frequency, and rain outcome counts. Pipe it anywhere:

```bash
python eda.py --csv weather.csv > eda_output.json
```

**Sample output:**
```json
{
  "kpis": { "avg_max_temp": 20.55, "rain_days": 66, ... },
  "monthly_stats": [ { "month": 1, "avg_max_temp": 25.1, ... }, ... ],
  "temp_distribution": { "<=10": 9, "11-15": 83, ... },
  ...
}
```

### Step 3 — Train & evaluate the model

```bash
python weather-dashboard/python/model.py --csv weather.csv
```

Outputs evaluation metrics to stdout and writes `results.json`:

```
── Model Evaluation ──────────────────────────────
  Rule      : IF Humidity3pm > 60% OR Rainfall > 1mm → RainTomorrow = Yes
  Accuracy  : 74.9%
  Precision : 39.5%
  Recall    : 74.2%
  F1 Score  : 51.6%
  Confusion : {'tp': 49, 'tn': 225, 'fp': 75, 'fn': 17}

── Feature Correlations (top 10) ─────────────────
  RISK_MM                0.892
  Humidity3pm            0.324
  Rainfall               0.301
  Cloud3pm               0.285
  ...

── Seasonal Rain Risk ────────────────────────────
  Summer    23 rain days / 90   (25.6%)
  Autumn    17 rain days / 90   (18.9%)
  Winter    12 rain days / 90   (13.3%)
  Spring    14 rain days / 90   (15.6%)
```

**Tune the thresholds:**
```bash
python model.py --csv weather.csv --humidity-threshold 65 --rain-threshold 2
```

---

## 📊 Frontend — Chart Modules

The frontend reads static constants from [`js/weatherData.js`](js/weatherData.js).  
After running `eda.py`, copy the updated values into that file to refresh the charts.

| JS file | What it does |
|---|---|
| `js/weatherData.js` | All data arrays & KPI constants |
| `js/charts.js` | `initTempChart()`, `initRainChart()`, `initTempDistChart()`, `initHumDistChart()`, `initCloudChart()`, `initWindChart()`, `initRainPieChart()` |

---

## 🚀 Running Locally

```bash
# 1. Run the Python pipeline
cd weather-dashboard/python
pip install -r requirements.txt
python eda.py   --csv ../../weather.csv
python model.py --csv ../../weather.csv

# 2. Open the frontend
cd ..
# open index.html in your browser, or:
npx serve .
# or:
python -m http.server 8080
```

---

## 📦 Dependencies

| Layer | Library | Version |
|---|---|---|
| Python | pandas | ≥ 2.0 |
| Python | numpy | ≥ 1.24 |
| Frontend | ECharts | 5.4.3 (CDN) |

---

## 📂 Data Source

`weather.csv` — 366 rows × 22 columns of daily weather observations.

Key columns:
`MinTemp`, `MaxTemp`, `Rainfall`, `Humidity3pm`, `Humidity9am`,
`WindGustDir`, `WindGustSpeed`, `Cloud9am`, `Pressure9am`, `RainToday`, `RainTomorrow`

---

*Made with [IBM Bob](https://www.ibm.com/products/watsonx)*
