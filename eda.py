"""
eda.py
------
Exploratory Data Analysis for weather.csv.
Computes every statistic used by the dashboard charts and prints
a JSON summary that can be piped into weatherData.js or used directly.

Usage:
    python eda.py                    # prints summary JSON to stdout
    python eda.py --csv ../weather.csv
"""

import json
import argparse
import numpy as np
import pandas as pd
from data import load_data


def compute_monthly_stats(df: pd.DataFrame, rows_per_month: int = 30) -> list[dict]:
    """
    Split dataset into 12 equal-sized monthly buckets and compute
    avg max/min temp, total rainfall, avg humidity, rain day count,
    avg wind gust for each bucket.

    Parameters
    ----------
    df : pd.DataFrame
    rows_per_month : int
        Rows to treat as one month (default 30).

    Returns
    -------
    list of dict — one entry per month
    """
    results = []
    for i in range(12):
        chunk = df.iloc[i * rows_per_month : (i + 1) * rows_per_month]
        results.append({
            "month": i + 1,
            "avg_max_temp":    round(chunk["MaxTemp"].mean(), 1),
            "avg_min_temp":    round(chunk["MinTemp"].mean(), 1),
            "total_rainfall":  round(chunk["Rainfall"].sum(), 1),
            "avg_humidity":    round(chunk["Humidity3pm"].mean(), 1),
            "rain_days":       int(chunk["RainToday"].sum()),
            "avg_wind_gust":   round(chunk["WindGustSpeed"].mean(), 1),
        })
    return results


def compute_temp_distribution(df: pd.DataFrame) -> dict:
    """Days per max-temperature band."""
    bins   = [-999, 10, 15, 20, 25, 30, 999]
    labels = ["<=10", "11-15", "16-20", "21-25", "26-30", ">30"]
    counts = pd.cut(df["MaxTemp"], bins=bins, labels=labels).value_counts().sort_index()
    return dict(zip(labels, counts.tolist()))


def compute_humidity_distribution(df: pd.DataFrame) -> dict:
    """Days per afternoon-humidity band."""
    bins   = [-1, 20, 40, 60, 80, 101]
    labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
    counts = pd.cut(df["Humidity3pm"], bins=bins, labels=labels).value_counts().sort_index()
    return dict(zip(labels, counts.tolist()))


def compute_cloud_distribution(df: pd.DataFrame) -> dict:
    """Days per cloud-cover band (oktas 0-8)."""
    bins   = [-1, 2, 5, 9]
    labels = ["Clear (0-2)", "Partly (3-5)", "Overcast (6-8)"]
    counts = pd.cut(df["Cloud9am"], bins=bins, labels=labels).value_counts().sort_index()
    return dict(zip(labels, counts.tolist()))


def compute_wind_direction_frequency(df: pd.DataFrame, top_n: int = 8) -> dict:
    """Top N wind gust directions by day count."""
    freq = (
        df["WindGustDir"]
        .dropna()
        .value_counts()
        .head(top_n)
        .sort_values()          # ascending so chart renders correctly
    )
    return freq.to_dict()


def compute_kpis(df: pd.DataFrame) -> dict:
    """Overall summary KPIs."""
    return {
        "total_rows":    len(df),
        "total_cols":    len(df.columns),
        "avg_max_temp":  round(df["MaxTemp"].mean(), 2),
        "avg_min_temp":  round(df["MinTemp"].mean(), 2),
        "peak_temp":     round(df["MaxTemp"].max(), 1),
        "lowest_temp":   round(df["MinTemp"].min(), 1),
        "avg_humidity":  round(df["Humidity3pm"].mean(), 2),
        "rain_days":     int(df["RainToday"].sum()),
        "avg_rainfall":  round(df["Rainfall"].mean(), 2),
        "avg_wind_gust": round(df["WindGustSpeed"].mean(), 1),
    }


def compute_rain_outcome_counts(df: pd.DataFrame) -> dict:
    """Yes/No counts for RainToday and RainTomorrow."""
    return {
        "rain_today_yes":     int(df["RainToday"].sum()),
        "rain_today_no":      int((~df["RainToday"]).sum()),
        "rain_tomorrow_yes":  int(df["RainTomorrow"].sum()),
        "rain_tomorrow_no":   int((~df["RainTomorrow"]).sum()),
    }


def run_eda(csv_path: str = "../weather.csv") -> dict:
    """Run full EDA and return a summary dict."""
    df = load_data(csv_path)
    return {
        "kpis":                   compute_kpis(df),
        "monthly_stats":          compute_monthly_stats(df),
        "temp_distribution":      compute_temp_distribution(df),
        "humidity_distribution":  compute_humidity_distribution(df),
        "cloud_distribution":     compute_cloud_distribution(df),
        "wind_direction_freq":    compute_wind_direction_frequency(df),
        "rain_outcomes":          compute_rain_outcome_counts(df),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EDA on weather.csv")
    parser.add_argument("--csv", default="../weather.csv", help="Path to weather.csv")
    args = parser.parse_args()

    summary = run_eda(args.csv)
    print(json.dumps(summary, indent=2))
