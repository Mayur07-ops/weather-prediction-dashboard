"""
data.py
-------
Loads and validates weather.csv into a clean pandas DataFrame.
All other Python modules import `load_data()` from here.

Usage:
    from data import load_data
    df = load_data("../weather.csv")
"""

import pandas as pd
from pathlib import Path

# Columns expected in the CSV
EXPECTED_COLUMNS = [
    "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
    "WindGustDir", "WindGustSpeed", "WindDir9am", "WindDir3pm",
    "WindSpeed9am", "WindSpeed3pm", "Humidity9am", "Humidity3pm",
    "Pressure9am", "Pressure3pm", "Cloud9am", "Cloud3pm",
    "Temp9am", "Temp3pm", "RainToday", "RISK_MM", "RainTomorrow",
]

# Numeric columns that may contain "NA" strings
NUMERIC_COLS = [
    "MinTemp", "MaxTemp", "Rainfall", "Evaporation", "Sunshine",
    "WindGustSpeed", "WindSpeed9am", "WindSpeed3pm",
    "Humidity9am", "Humidity3pm", "Pressure9am", "Pressure3pm",
    "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RISK_MM",
]


def load_data(csv_path: str | Path = "weather.csv") -> pd.DataFrame:
    """
    Load weather.csv into a clean DataFrame.

    Steps:
      1. Read CSV, coerce 'NA' strings to NaN.
      2. Cast numeric columns to float.
      3. Impute missing values with the column median.
      4. Encode RainToday / RainTomorrow as boolean (True = Yes).

    Parameters
    ----------
    csv_path : str or Path
        Path to weather.csv (default: 'weather.csv' in cwd).

    Returns
    -------
    pd.DataFrame
        Clean DataFrame ready for EDA and modelling.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path.resolve()}")

    df = pd.read_csv(path, na_values=["NA", "N/A", ""])

    # Cast numeric columns
    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Impute missing numeric values with column median
    missing_before = df[NUMERIC_COLS].isna().sum().sum()
    for col in NUMERIC_COLS:
        if col in df.columns and df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    missing_after = df[NUMERIC_COLS].isna().sum().sum()
    print(f"[data] Loaded {len(df)} rows × {len(df.columns)} columns")
    print(f"[data] Imputed {missing_before} missing values → {missing_after} remaining")

    # Encode rain flags as boolean
    for col in ("RainToday", "RainTomorrow"):
        if col in df.columns:
            df[col] = df[col].str.strip().str.lower().map({"yes": True, "no": False})

    return df


if __name__ == "__main__":
    df = load_data("../weather.csv")
    print(df.describe())
