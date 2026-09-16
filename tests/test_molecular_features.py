import pandas as pd
from src.molecular_features import parse_smiles, compute_morgan, compute_descriptors

def test_valid_smiles():
    mol = parse_smiles("CCO")
    assert mol is not None
    assert len(compute_morgan(mol)) == 2048
    assert compute_descriptors(mol)["MolWt"] > 0

def test_invalid_smiles():
    assert parse_smiles("not-a-smiles") is None
