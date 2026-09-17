from __future__ import annotations
import re
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

def split_reactions(value):
    if pd.isna(value):
        return []
    return [x.strip().lower() for x in re.split(r"[;|]+", str(value)) if x.strip()]

def prepare_drug_ae_pairs(df):
    work = df[["report_id", "suspect_drug", "reactions", "primary_reaction"]].copy()
    work["drug"] = work["suspect_drug"].fillna("UNKNOWN").astype(str).str.strip().str.upper()
    work["reaction_list"] = work["reactions"].map(split_reactions)
    work["reaction_list"] = work.apply(
        lambda r: r["reaction_list"] if r["reaction_list"] else [str(r["primary_reaction"]).strip().lower()],
        axis=1
    )
    pairs = work.explode("reaction_list").rename(columns={"reaction_list": "ae"})
    pairs["ae"] = pairs["ae"].fillna("unknown").astype(str).str.strip()
    return pairs[["report_id", "drug", "ae"]].drop_duplicates()

def disproportionality(a, b, c, d):
    total_drug = a + b
    total_non_drug = c + d
    prr = np.nan if total_drug == 0 or total_non_drug == 0 else (
        (a / total_drug) / (c / total_non_drug) if c > 0 else np.inf
    )
    ror = np.inf if b == 0 or c == 0 else (a * d) / (b * c)
    try:
        chi2, p, _, _ = chi2_contingency([[a,b],[c,d]], correction=False)
    except ValueError:
        chi2, p = np.nan, np.nan
    return prr, ror, chi2, p

def compute_signals(df, min_count=3):
    pairs = prepare_drug_ae_pairs(df)
    N = pairs["report_id"].nunique()
    drug_counts = pairs[["report_id","drug"]].drop_duplicates()["drug"].value_counts()
    ae_counts = pairs[["report_id","ae"]].drop_duplicates()["ae"].value_counts()
    pair_counts = pairs.groupby(["drug","ae"]).size()

    rows = []
    for (drug, ae), a in pair_counts.items():
        drug_total = int(drug_counts.get(drug, 0))
        ae_total = int(ae_counts.get(ae, 0))
        b, c, d = drug_total-a, ae_total-a, N-a-(drug_total-a)-(ae_total-a)
        if min(a,b,c,d) < 0:
            continue
        prr, ror, chi2, p = disproportionality(int(a), int(b), int(c), int(d))
        rows.append({
            "suspect_drug": drug, "ae": ae, "a": int(a), "b": int(b),
            "c": int(c), "d": int(d), "PRR": prr, "ROR": ror,
            "chi2": chi2, "p_value": p,
            "evans_signal": bool(a >= min_count and prr >= 2 and chi2 >= 4)
        })
    return pd.DataFrame(rows)

def rank_signals(signals):
    if signals.empty:
        return signals.copy()
    out = signals.copy()
    out["signal_strength"] = (
        np.log1p(out["PRR"].replace([np.inf], np.nan).fillna(0).clip(lower=0)) +
        0.25*np.log1p(out["chi2"].replace([np.inf], np.nan).fillna(0).clip(lower=0))
    )
    return out.sort_values("signal_strength", ascending=False)
