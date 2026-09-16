# Methodology

1. **Tox21 EDA:** assess missingness, endpoint balance, co-occurrence, and chemical-space descriptors.
2. **Molecular representation:** parse SMILES; calculate Morgan/ECFP4 fingerprints (radius 2, 2048 bits) plus curated RDKit descriptors.
3. **Modeling:** train endpoint-specific Random Forest classifiers with median imputation and class-balanced learning.
4. **Validation:** prefer scaffold-aware splitting to estimate generalization to chemically distinct structures.
5. **Evaluation:** ROC-AUC, PR-AUC, accuracy, F1, confusion matrices; PR-AUC is emphasized for imbalanced endpoints.
6. **Calibration:** isotonic calibration can be applied to a selected endpoint.
7. **Interpretability:** SHAP explains model behavior; it does not establish biological causality.
8. **FAERS:** calculate PRR, ROR, chi-squared, and Evans-style screening criteria.
9. **Integration:** combine Tox21 pathway predictions and FAERS evidence using transparent, configurable weights.

All integrated scores are ranking/triage scores, not probabilities of clinical harm.
