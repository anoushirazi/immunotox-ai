from __future__ import annotations
from typing import Dict
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score

def make_model(random_state=42, n_estimators=500) -> Pipeline:
    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", RandomForestClassifier(
            n_estimators=n_estimators,
            class_weight="balanced_subsample",
            random_state=random_state,
            n_jobs=-1,
            min_samples_leaf=2,
            max_features="sqrt"
        ))
    ])

def evaluate_binary(y_true, probability, threshold=0.5) -> Dict[str, float]:
    y_true = np.asarray(y_true).astype(int)
    pred = (np.asarray(probability) >= threshold).astype(int)
    out = {
        "n": len(y_true),
        "accuracy": accuracy_score(y_true, pred),
        "f1": f1_score(y_true, pred, zero_division=0),
        "roc_auc": np.nan,
        "pr_auc": np.nan,
    }
    if len(np.unique(y_true)) == 2:
        out["roc_auc"] = roc_auc_score(y_true, probability)
        out["pr_auc"] = average_precision_score(y_true, probability)
    return out

def fit_endpoint_models(X, Y, train_idx, test_idx, random_state=42):
    models, metrics = {}, []
    for endpoint in Y.columns:
        y = Y[endpoint]
        tr = [i for i in train_idx if pd.notna(y.iloc[i])]
        te = [i for i in test_idx if pd.notna(y.iloc[i])]
        if len(tr) < 20 or y.iloc[tr].nunique() < 2 or not te:
            continue
        model = make_model(random_state)
        model.fit(X.iloc[tr], y.iloc[tr].astype(int))
        p = model.predict_proba(X.iloc[te])[:, 1]
        row = evaluate_binary(y.iloc[te], p)
        row["endpoint"] = endpoint
        models[endpoint] = model
        metrics.append(row)
    return models, pd.DataFrame(metrics)

def calibrate_model(base_model, X_train, y_train, method="isotonic"):
    calibrated = CalibratedClassifierCV(base_model, method=method, cv=3)
    calibrated.fit(X_train, y_train.astype(int))
    return calibrated

def save_models(models: Dict[str, object], directory):
    from pathlib import Path
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for endpoint, model in models.items():
        name = endpoint.replace("/", "_").replace("-", "_")
        joblib.dump(model, directory / f"{name}.joblib")
