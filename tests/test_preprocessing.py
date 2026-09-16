import pandas as pd
from src.preprocessing import normalize_name, flag_immune_reactions

def test_normalize_name():
    assert normalize_name("  Drug A  ") == "DRUG A"

def test_immune_flag():
    s = pd.Series(["anaphylaxis", "headache", "hypersensitivity"])
    assert flag_immune_reactions(s).tolist() == [True, False, True]
