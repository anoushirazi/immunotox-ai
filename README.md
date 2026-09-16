# ImmunoToxAI
AI-powered immunotoxicity and adverse event risk assessment for early-stage drug development.

## Predictive Immunotoxicity and Adverse Event Risk Assessment for Early Drug Development

ImmunoToxAI is a portfolio-ready biotech ML project that connects:

**Tox21 molecular assay evidence → ML toxicity prediction → FAERS pharmacovigilance signals → interpretable integrated risk prioritization**

### Scientific objective
The system is designed to help R&D teams prioritize candidates for additional safety investigation. It is a decision-support and hypothesis-generation system, not a clinical causality engine.

### Data
Place the supplied datasets here:
```text
data/raw/tox21/tox21.csv
data/raw/faers/fda_adverse_events_2015_2026_CLEAN.csv
```

### Run order
1. `01_Tox21_EDA.ipynb`
2. `02_Molecular_Features.ipynb`
3. `03_Toxicity_Model.ipynb`
4. `04_FAERS_EDA.ipynb`
5. `05_AE_Signal_Detection.ipynb`
6. `06_Integrated_Risk_Engine.ipynb`

### Install
```bash
python -m pip install -r requirements.txt
```

### Tests
```bash
pytest -q
```

### Dashboard
```bash
streamlit run dashboard/app.py
```

### Project principles
- Reproducible paths and configuration.
- Missing labels treated as unknown.
- Scaffold-aware validation where feasible.
- PR-AUC emphasized for imbalanced endpoints.
- Probability calibration for selected models.
- SHAP for model interpretation.
- Transparent FAERS disproportionality metrics.
- Explicit separation between association, signal detection, and causality.
- Domain-expert review required before operational use.

### Important limitations
FAERS is subject to reporting bias, confounding, missing exposure denominators, and other pharmacovigilance limitations. Tox21 is a collection of pathway-level assays and does not represent all human immunotoxicity. The integrated score is a prioritization score, not a clinical risk probability.

### Portfolio positioning
This repository demonstrates practical skills across cheminformatics, classical ML, model evaluation, explainable AI, pharmacovigilance analytics, reproducible engineering, and biotech decision-support design.

## 📁 Project Structure

```text
ImmunoToxAI/
│
├── data/
│   ├── raw/
│   │   ├── tox21/
│   │   ├── faers/
│   │   └── drug_mapping/
│   ├── processed/
│   │   ├── tox21/
│   │   ├── faers/
│   │   └── integrated/
│   └── reference/
│       ├── immune_ae_dictionary.csv
│       ├── drug_name_synonyms.csv
│       └── pathway_weights.yaml
│
├── configs/
│   ├── config.yaml
│   ├── tox21.yaml
│   └── faers.yaml
│
├── notebooks/
│   ├── 01_Tox21_EDA.ipynb
│   ├── 02_Molecular_Features.ipynb
│   ├── 03_Toxicity_Model.ipynb
│   ├── 04_FAERS_EDA.ipynb
│   ├── 05_AE_Signal_Detection.ipynb
│   └── 06_Integrated_Risk_Engine.ipynb
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── molecular_features.py
│   ├── tox21_model.py
│   ├── faers_signals.py
│   ├── drug_mapping.py
│   ├── risk_engine.py
│   ├── evaluation.py
│   └── visualization.py
│
├── models/
│   ├── tox21/
│   │   ├── tox21_multitask_model.pkl
│   │   ├── calibration_models/
│   │   └── metadata.json
│   └── faers/
│       ├── ae_signal_model.pkl
│       └── metadata.json
│
├── dashboard/
│   └── app.py
│
├── reports/
│   ├── figures/
│   └── model_cards/
│
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   ├── model_card.md
│   └── limitations.md
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_molecular_features.py
│   ├── test_faers_signals.py
│   └── test_risk_engine.py
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

