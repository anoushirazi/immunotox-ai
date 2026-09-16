import pandas as pd
from src.faers_signals import disproportionality, prepare_drug_ae_pairs

def test_disproportionality():
    prr, ror, chi2, p = disproportionality(10, 10, 5, 75)
    assert prr > 1
    assert ror > 1

def test_pairs():
    df = pd.DataFrame({
        "report_id":[1,2],
        "suspect_drug":["A","A"],
        "reactions":["rash;fever","headache"],
        "primary_reaction":["rash","headache"]
    })
    pairs = prepare_drug_ae_pairs(df)
    assert len(pairs) == 3
