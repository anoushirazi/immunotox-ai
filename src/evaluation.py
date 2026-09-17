from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, confusion_matrix

def binary_metrics(y_true, y_prob, threshold=0.5):
    y_true = np.asarray(y_true).astype(int)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)
    result = {
        "n": len(y_true),
        "threshold": threshold,
        "sensitivity": np.nan,
        "specificity": np.nan,
        "roc_auc": np.nan,
        "pr_auc": np.nan,
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
    }
    cm = confusion_matrix(y_true, y_pred, labels=[0,1])
    tn, fp, fn, tp = cm.ravel()
    result["sensitivity"] = tp/(tp+fn) if tp+fn else np.nan
    result["specificity"] = tn/(tn+fp) if tn+fp else np.nan
    if len(np.unique(y_true)) == 2:
        result["roc_auc"] = roc_auc_score(y_true, y_prob)
        result["pr_auc"] = average_precision_score(y_true, y_prob)
    return result

def summarize_endpoint_results(results):
    if results.empty:
        return results
    return results.sort_values(["pr_auc","roc_auc"], ascending=False)
