from __future__ import annotations
import numpy as np
import pandas as pd

DEFAULT_WEIGHTS = {"toxicity": 0.55, "faers": 0.30, "seriousness": 0.15}

def minmax(series):
    s = pd.Series(series, dtype=float)
    if len(s) == 0 or s.max() == s.min():
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.min()) / (s.max() - s.min())

def toxicity_component(predictions: pd.DataFrame, weights=None):
    weights = weights or {c: 1.0 for c in predictions.columns}
    cols = [c for c in predictions.columns if c in weights]
    if not cols:
        return pd.Series(0.0, index=predictions.index)
    w = np.array([weights[c] for c in cols], dtype=float)
    return predictions[cols].mul(w, axis=1).sum(axis=1) / w.sum()

def build_integrated_score(toxicity, faers, seriousness, weights=None):
    weights = weights or DEFAULT_WEIGHTS
    return (
        weights["toxicity"] * pd.Series(toxicity).fillna(0) +
        weights["faers"] * pd.Series(faers).fillna(0) +
        weights["seriousness"] * pd.Series(seriousness).fillna(0)
    )

def classify_risk(score):
    if score < 0.33:
        return "Lower"
    if score < 0.66:
        return "Intermediate"
    return "Higher"
