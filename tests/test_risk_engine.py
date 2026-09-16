import pandas as pd
from src.risk_engine import toxicity_component, build_integrated_score, classify_risk

def test_toxicity_component():
    x = pd.DataFrame({"NR-ER":[0.2,0.8], "SR-ARE":[0.4,0.6]})
    out = toxicity_component(x)
    assert list(out.round(2)) == [0.3,0.7]

def test_risk_score():
    score = build_integrated_score([0.8], [0.4], [0.2]).iloc[0]
    assert 0 <= score <= 1
    assert classify_risk(score) in {"Lower","Intermediate","Higher"}
