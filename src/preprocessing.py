from __future__ import annotations
import re
from typing import Iterable
import numpy as np
import pandas as pd

TOX21_ENDPOINTS = [
    "NR-AR", "NR-AR-LBD", "NR-AhR", "NR-Aromatase",
    "NR-ER", "NR-ER-LBD", "NR-PPAR-gamma",
    "SR-ARE", "SR-ATAD5", "SR-HSE", "SR-MMP", "SR-p53"
]

DEFAULT_IMMUNE_TERMS = [
    "hypersensitivity", "anaphylaxis", "anaphylactic", "immune",
    "immun", "autoimmune", "cytokine", "urticaria", "angioedema",
    "allergic", "allergy", "serum sickness", "vasculitis",
    "immune-mediated", "interstitial nephritis"
]

def load_tox21(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_faers(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def endpoint_quality(df: pd.DataFrame, endpoints: Iterable[str] = TOX21_ENDPOINTS) -> pd.DataFrame:
    endpoints = list(endpoints)
    return pd.DataFrame({
        "dtype": df[endpoints].dtypes.astype(str),
        "missing_n": df[endpoints].isna().sum(),
        "missing_pct": df[endpoints].isna().mean() * 100,
        "unique_n": df[endpoints].nunique(dropna=True),
    })

def endpoint_balance(df: pd.DataFrame, endpoints: Iterable[str] = TOX21_ENDPOINTS) -> pd.DataFrame:
    rows = []
    for col in endpoints:
        y = pd.to_numeric(df[col], errors="coerce")
        n = y.notna().sum()
        pos = (y == 1).sum()
        rows.append({
            "endpoint": col, "n_valid": int(n), "positive": int(pos),
            "negative": int((y == 0).sum()),
            "positive_pct": 100 * pos / n if n else np.nan
        })
    return pd.DataFrame(rows)

def normalize_name(value) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().upper())

def flag_immune_reactions(series: pd.Series, terms=None) -> pd.Series:
    terms = terms or DEFAULT_IMMUNE_TERMS
    pattern = re.compile("|".join(re.escape(t) for t in terms), re.IGNORECASE)
    return series.fillna("").astype(str).str.contains(pattern, na=False)

def serious_report_flag(df: pd.DataFrame) -> pd.Series:
    def bool_col(name):
        if name not in df:
            return pd.Series(False, index=df.index)
        s = df[name]
        return s.astype(str).str.lower().isin(["1", "true", "yes", "y"])
    return (
        bool_col("serious") |
        bool_col("is_fatal") |
        bool_col("is_hospitalized") |
        bool_col("is_life_threat") |
        bool_col("is_disabling")
    )
