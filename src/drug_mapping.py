from __future__ import annotations
import pandas as pd

def load_synonyms(path):
    return pd.read_csv(path)

def normalize_drug_name(value):
    return "" if pd.isna(value) else str(value).strip().upper()

def apply_synonyms(df, drug_col="suspect_drug", synonyms=None):
    out = df.copy()
    out["canonical_drug"] = out[drug_col].map(normalize_drug_name)
    if synonyms is not None and not synonyms.empty:
        mapping = {
            str(r["synonym"]).strip().upper(): str(r["canonical_name"]).strip().upper()
            for _, r in synonyms.iterrows()
        }
        out["canonical_drug"] = out["canonical_drug"].map(lambda x: mapping.get(x, x))
    return out

def map_class_to_endpoints(drug_name, mapping_df):
    if mapping_df.empty:
        return []
    rows = mapping_df[
        mapping_df["drug_or_compound"].astype(str).str.upper().eq(str(drug_name).upper())
    ]
    if rows.empty:
        return []
    return [x.strip() for x in str(rows.iloc[0].get("mapped_tox21_endpoints","")).split(";") if x.strip()]
