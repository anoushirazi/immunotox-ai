from __future__ import annotations
from typing import Dict, Tuple
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem, Descriptors, Lipinski

DESCRIPTORS = {
    "MolWt": Descriptors.MolWt,
    "MolLogP": Descriptors.MolLogP,
    "TPSA": Descriptors.TPSA,
    "HBA": Lipinski.NumHAcceptors,
    "HBD": Lipinski.NumHDonors,
    "RotatableBonds": Lipinski.NumRotatableBonds,
    "RingCount": Lipinski.RingCount,
    "HeavyAtomCount": Lipinski.HeavyAtomCount,
    "FractionCSP3": Lipinski.FractionCSP3,
}

def parse_smiles(smiles):
    if pd.isna(smiles):
        return None
    try:
        return Chem.MolFromSmiles(str(smiles))
    except Exception:
        return None

def compute_morgan(mol, radius: int = 2, n_bits: int = 2048) -> np.ndarray:
    arr = np.zeros(n_bits, dtype=np.uint8)
    if mol is None:
        return arr
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr

def compute_descriptors(mol) -> Dict[str, float]:
    if mol is None:
        return {name: np.nan for name in DESCRIPTORS}
    out = {}
    for name, func in DESCRIPTORS.items():
        try:
            out[name] = float(func(mol))
        except Exception:
            out[name] = np.nan
    return out

def featurize_smiles(smiles: pd.Series, radius=2, n_bits=2048) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    molecules = smiles.map(parse_smiles)
    desc = pd.DataFrame([compute_descriptors(m) for m in molecules], index=smiles.index)
    fps = pd.DataFrame(
        np.vstack([compute_morgan(m, radius, n_bits) for m in molecules]),
        columns=[f"ECFP4_{i}" for i in range(n_bits)],
        index=smiles.index
    )
    return pd.concat([desc, fps], axis=1), desc, molecules.isna()
