"""
model.py
--------
Rain prediction model — naive rule-based classifier derived from
feature correlation analysis on weather.csv.

Rule:
    IF Humidity3pm > 60  OR  Rainfall > 1  →  RainTomorrow = True

Also provides:
  - Feature correlation analysis
  - Full evaluation metrics (accuracy, precision, recall, F1)
  - Confusion matrix
  - Seasonal rain risk summary
  - export_results_json() — writes results.json for the dashboard

Usage:
    python model.py                        # prints metrics + writes results.json
    python model.py --csv ../weather.csv
    python model.py --csv ../weather.csv --humidity-threshold 65 --rain-threshold 2
"""

import json
import argparse
import numpy as np
import pandas as pd
from pathlib import Path
from data import load_data


# ── Rule thresholds (tuneable via CLI) ─────────────────────────────────────
DEFAULT_HUMIDITY_THRESHOLD = 60   # Humidity3pm (%)
DEFAULT_RAIN_THRESHOLD     = 1    # Rainfall (mm)


def predict_rain(
    humidity_3pm: float,
    rainfall_today: float,
    humidity_threshold: float = DEFAULT_HUMIDITY_THRESHOLD,
    rain_threshold: float = DEFAULT_RAIN_THRESHOLD,
) -> bool:
    """
    Predict whether it will rain tomorrow using the rule-based classifier.

    Parameters
    ----------
    humidity_3pm       : afternoon humidity reading (%)
    rainfall_today     : today's rainfall (mm)
    humidity_threshold : humidity cutoff (default 60)
    rain_threshold     : rainfall cutoff in mm (default 1)

    Returns
    -------
    bool — True if rain is predicted tomorrow
    """
    return humidity_3pm > humidity_threshold or rainfall_today > rain_threshold


def predict_series(
    df: pd.DataFrame,
    humidity_threshold: float = DEFAULT_HUMIDITY_THRESHOLD,
    rain_threshold: float = DEFAULT_RAIN_THRESHOLD,
) -> pd.Series:
    """
    Apply predict_rain() to every row of the DataFrame.

    Returns
    -------
    pd.Series of bool — predicted RainTomorrow for each row
    """
    return df.apply(
        lambda row: predict_rain(
            row["Humidity3pm"], row["Rainfall"],
            humidity_threshold, rain_threshold,
        ),
        axis=1,
    )


def confusion_matrix(actual: pd.Series, predicted: pd.Series) -> dict:
    """Return TP, TN, FP, FN counts."""
    tp = int(( actual &  predicted).sum())
    tn = int((~actual & ~predicted).sum())
    fp = int((~actual &  predicted).sum())
    fn = int(( actual & ~predicted).sum())
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn}


def evaluate(
    df: pd.DataFrame,
    humidity_threshold: float = DEFAULT_HUMIDITY_THRESHOLD,
    rain_threshold: float = DEFAULT_RAIN_THRESHOLD,
) -> dict:
    """
    Evaluate the rule-based model on the full dataset.

    Returns
    -------
    dict with accuracy, precision, recall, f1, and confusion matrix
    """
    actual    = df["RainTomorrow"]
    predicted = predict_series(df, humidity_threshold, rain_threshold)

    cm       = confusion_matrix(actual, predicted)
    tp, tn, fp, fn = cm["tp"], cm["tn"], cm["fp"], cm["fn"]

    accuracy  = round((tp + tn) / len(df) * 100, 1)
    precision = round(tp / (tp + fp) * 100, 1) if (tp + fp) > 0 else 0.0
    recall    = round(tp / (tp + fn) * 100, 1) if (tp + fn) > 0 else 0.0
    f1        = round(
        2 * precision * recall / (precision + recall), 1
    ) if (precision + recall) > 0 else 0.0

    return {
        "accuracy":   accuracy,
        "precision":  precision,
        "recall":     recall,
        "f1_score":   f1,
        "samples":    len(df),
        "confusion_matrix": cm,
        "thresholds": {
            "humidity_3pm": humidity_threshold,
            "rainfall_mm":  rain_threshold,
        },
        "rule": (
            f"IF Humidity3pm > {humidity_threshold}% "
            f"OR Rainfall > {rain_threshold}mm → RainTomorrow = Yes"
        ),
    }


def feature_correlations(df: pd.DataFrame) -> dict:
    """
    Compute Pearson correlation of numeric features with RainTomorrow (1/0).
    Returns dict sorted by absolute correlation descending.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    target     = df["RainTomorrow"].astype(int)
    corr       = numeric_df.corrwith(target).dropna().abs().sort_values(ascending=False)
    return {col: round(float(val), 3) for col, val in corr.items() if col != "RainTomorrow"}


def seasonal_rain_risk(df: pd.DataFrame, rows_per_month: int = 30) -> list[dict]:
    """
    Aggregate rain day counts by season (4 groups of 3 months).
    """
    season_map = {
        "Summer": (0, 3),
        "Autumn": (3, 6),
        "Winter": (6, 9),
        "Spring": (9, 12),
    }
    results = []
    for season, (start_m, end_m) in season_map.items():
        chunk = df.iloc[start_m * rows_per_month : end_m * rows_per_month]
        days  = int(chunk["RainToday"].sum())
        total = len(chunk)
        results.append({
            "season":    season,
            "rain_days": days,
            "total_days": total,
            "risk_pct":  round(days / total * 100, 1) if total > 0 else 0,
        })
    return results


def export_results_json(
    df: pd.DataFrame,
    out_path: str | Path = "results.json",
    humidity_threshold: float = DEFAULT_HUMIDITY_THRESHOLD,
    rain_threshold: float = DEFAULT_RAIN_THRESHOLD,
) -> None:
    """
    Write full model evaluation + feature correlations + seasonal risk
    to a JSON file consumable by the frontend dashboard.
    """
    results = {
        "evaluation":           evaluate(df, humidity_threshold, rain_threshold),
        "feature_correlations": feature_correlations(df),
        "seasonal_risk":        seasonal_rain_risk(df),
    }
    Path(out_path).write_text(json.dumps(results, indent=2))
    print(f"[model] Results written to {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate rain prediction model")
    parser.add_argument("--csv",                default="../weather.csv")
    parser.add_argument("--humidity-threshold", type=float, default=DEFAULT_HUMIDITY_THRESHOLD)
    parser.add_argument("--rain-threshold",     type=float, default=DEFAULT_RAIN_THRESHOLD)
    parser.add_argument("--out",                default="results.json")
    args = parser.parse_args()

    df = load_data(args.csv)

    metrics = evaluate(df, args.humidity_threshold, args.rain_threshold)
    print("\n── Model Evaluation ──────────────────────────────")
    print(f"  Rule      : {metrics['rule']}")
    print(f"  Accuracy  : {metrics['accuracy']}%")
    print(f"  Precision : {metrics['precision']}%")
    print(f"  Recall    : {metrics['recall']}%")
    print(f"  F1 Score  : {metrics['f1_score']}%")
    print(f"  Confusion : {metrics['confusion_matrix']}")

    print("\n── Feature Correlations (top 10) ─────────────────")
    for feat, val in list(feature_correlations(df).items())[:10]:
        print(f"  {feat:<22} {val}")

    print("\n── Seasonal Rain Risk ────────────────────────────")
    for s in seasonal_rain_risk(df):
        print(f"  {s['season']:<8}  {s['rain_days']} rain days / {s['total_days']}  ({s['risk_pct']}%)")

    export_results_json(df, args.out, args.humidity_threshold, args.rain_threshold)
