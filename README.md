# ImmunoToxAI

## AI-Powered Immunotoxicity and Adverse Event Risk Assessment for Early-Stage Drug Development

**ImmunoToxAI** is an end-to-end biotech machine learning project that combines **molecular toxicity prediction** with **real-world pharmacovigilance signals** to help prioritize drug candidates for additional safety investigation.

The project connects two complementary sources of safety evidence:

```text
Tox21 Molecular Assay Data
          │
          ▼
Molecular Feature Engineering
          │
          ▼
ML-Based Toxicity Prediction
          │
          ├──────────────┐
          │              │
          ▼              ▼
   Model Explainability   Calibration
          │
          │
          └──────────────┐
                         │
FAERS Adverse Event Data │
          │              │
          ▼              │
AE Signal Detection      │
          │              │
          └──────┬───────┘
                 ▼
       Integrated Risk Engine
                 │
                 ▼
      Risk Prioritization / Review

```

> **Important:** ImmunoToxAI is a research and educational decision-support prototype. It is intended for hypothesis generation and candidate prioritization, not for clinical diagnosis, regulatory decision-making, or establishing drug-event causality.

---

## 🔬 Scientific Objective

Early-stage drug development generates large amounts of heterogeneous safety information.

A molecule may show concerning activity in experimental toxicity assays, while another compound may appear relatively safe in laboratory assays but later produce adverse-event signals in real-world reporting data.

ImmunoToxAI explores how these two evidence streams can be analyzed together.

The primary objective is to build a reproducible ML pipeline that can:

1. Analyze molecular toxicity assay data from **Tox21**.
2. Generate molecular representations and predictive features.
3. Train machine learning models for toxicity-related endpoints.
4. Evaluate models using metrics appropriate for imbalanced toxicity datasets.
5. Explain model predictions using interpretable ML techniques.
6. Analyze **FAERS** adverse-event reports for potential safety signals.
7. Identify drug-event associations using pharmacovigilance disproportionality methods.
8. Map drug names and adverse events across datasets.
9. Integrate complementary evidence into a transparent prioritization score.
10. Produce interpretable outputs for further scientific review.

---

# 🧬 What Problem Does ImmunoToxAI Address?

Traditional drug-safety analysis often requires combining multiple evidence sources that were not originally designed to work together.

This project demonstrates a computational framework for bringing together:

| Evidence Source                 | What It Provides                                                    |
| ------------------------------- | ------------------------------------------------------------------- |
| **Tox21**                       | Experimental molecular/pathway-level toxicity evidence              |
| **ML models**                   | Predicted toxicity-related activity                                 |
| **SHAP / XAI**                  | Explanation of important molecular features                         |
| **FAERS**                       | Real-world adverse-event reporting signals                          |
| **Disproportionality analysis** | Statistical identification of unusual drug-event reporting patterns |
| **Integrated Risk Engine**      | Transparent prioritization of candidates requiring further review   |

The system does **not** treat these signals as equivalent evidence.

Instead, it keeps the distinction between:

```text
Association
    ↓
Signal Detection
    ↓
Risk Prioritization
    ↓
Scientific Review
    ↓
Causality Assessment

```

This distinction is important because a statistical association in FAERS does not by itself demonstrate that a drug caused an adverse event.

---

# 🧪 Data Sources

## 1. Tox21

The **Tox21** program provides high-throughput toxicity screening data covering multiple biological pathways and assay endpoints.

In ImmunoToxAI, Tox21 is used to explore relationships between molecular characteristics and toxicity-related assay outcomes.

The project uses the dataset as an experimental source for:

- Exploratory data analysis
- Molecular feature generation
- Toxicity prediction
- Class-imbalance analysis
- Model evaluation
- Explainability

**Primary source:** U.S. EPA Tox21 data.

A downloadable project copy is also provided through the project data repository/reference location.

---

## 2. FAERS

The **FDA Adverse Event Reporting System (FAERS)** contains spontaneous reports of adverse events and medication-related safety information.

ImmunoToxAI uses FAERS data for exploratory pharmacovigilance analysis, including:

- Drug-event frequency analysis
- Adverse-event filtering
- Immune-related adverse-event identification
- Drug name normalization
- Signal detection
- Disproportionality analysis
- Candidate risk prioritization

### Important FAERS limitation

FAERS is a spontaneous reporting system.

Therefore, the data can be affected by:

- Reporting bias
- Under-reporting
- Duplicate reports
- Missing information
- Confounding
- Reporting stimulated by publicity
- Changes in reporting behavior
- Lack of reliable exposure denominators

Consequently:

> **A FAERS signal should be interpreted as a hypothesis-generating safety signal, not proof of causality.**

---

# 📊 Dataset Locations

Place the project original datasets in: 
[[Download](https://drive.google.com/file/d/1wy4frw6f8JdJwUWaNGKbIaL4qv-Dd7B_/view?usp=sharing)]

```text
data/raw/tox21/tox21.csv
data/raw/faers/fda_adverse_events_2015_2026_CLEAN.csv

```

The repository intentionally separates raw, processed, reference, and model-generated data. 
[[Download](https://drive.google.com/file/d/1z6Js1NkctPtapopVSVquN_vhRdD7UrXg/view?usp=sharing)]

Recommended structure:

```text
data/
├── raw/
│   ├── tox21/
│   ├── faers/
│   └── drug_mapping/
│
├── processed/
│   ├── tox21/
│   ├── faers/
│   └── integrated/
│
└── reference/
    ├── immune_ae_dictionary.csv
    ├── drug_name_synonyms.csv
    └── pathway_weights.yaml

```

Large datasets should generally **not** be committed directly to GitHub. The repository can contain download instructions and data documentation while the actual large files remain in external storage.

---

# 🧠 Machine Learning Pipeline

## Step 1 — Tox21 Exploratory Data Analysis

`01_Tox21_EDA.ipynb`

This notebook examines:

- Dataset dimensions
- Missing values
- Label distributions
- Assay distributions
- Class imbalance
- Duplicate records
- Endpoint characteristics
- Potential data-quality problems

The goal is to understand the structure of the data before modeling.

---

## Step 2 — Molecular Feature Engineering

`02_Molecular_Features.ipynb`

Molecular information is transformed into machine-learning-compatible representations.

Depending on the available molecular identifiers, the pipeline can include:

- Molecular descriptors
- Fingerprint-based representations
- Structure-derived features
- Feature filtering
- Missing-value handling
- Feature normalization where appropriate

The resulting feature matrix is used by downstream toxicity models.

---

## Step 3 — Toxicity Modeling

`03_Toxicity_Model.ipynb`

The toxicity modeling stage trains and evaluates ML models against selected Tox21 endpoints.

Potential model families include:

- Logistic Regression
- Random Forest
- Gradient Boosting
- Other tree-based models
- Multitask models where appropriate

Model selection is based on validation performance rather than simply maximizing accuracy.

### Evaluation metrics

Because toxicity endpoints can be highly imbalanced, the project emphasizes:

- **PR-AUC**
- ROC-AUC
- Precision
- Recall
- F1-score
- Confusion matrix
- Calibration metrics

PR-AUC is particularly useful when the positive toxicity class is relatively rare.

---

# 🔍 Explainable AI

Model performance alone is not sufficient for scientific interpretation.

ImmunoToxAI incorporates explainability methods such as **SHAP** to investigate which molecular features contribute to model predictions.

The goal is to answer questions such as:

```text
Why did the model assign this compound a higher predicted toxicity risk?

```

Rather than producing only:

```text
Risk = 0.82

```

the system attempts to provide additional information about the features contributing to the prediction.

This supports model auditing and scientific hypothesis generation.

---

# 💊 Pharmacovigilance Pipeline

## Step 4 — FAERS Exploratory Data Analysis

`04_FAERS_EDA.ipynb`

This stage examines:

- Drug-report frequencies
- Adverse-event frequencies
- Time distributions
- Missing values
- Duplicate or repeated records
- Drug-name variation
- Event terminology
- Potential immune-related adverse events

---

## Step 5 — Adverse Event Signal Detection

`05_AE_Signal_Detection.ipynb`

Potential drug-event associations are investigated using pharmacovigilance signal-detection methods.

Depending on the implementation, the analysis may include disproportionality metrics such as:

- Reporting Odds Ratio (ROR)
- Proportional Reporting Ratio (PRR)
- Confidence intervals
- Minimum report-count thresholds

Conceptually:

```text
Drug
  │
  ├── Number of reports
  │
  ├── Adverse event
  │
  ├── Background reporting frequency
  │
  └── Disproportionality statistic
             │
             ▼
       Safety Signal

```

A detected signal indicates that further investigation may be warranted. It does **not** establish a causal relationship.

---

# 🔗 Drug and Adverse Event Mapping

Real-world pharmacovigilance datasets contain substantial naming variability.

The project therefore includes mapping resources such as:

```text
drug_mapping/
├── drug_name_synonyms.csv
└── immune_ae_dictionary.csv

```

These resources help standardize:

- Drug names
- Drug synonyms
- Adverse-event terminology
- Immune-related event categories

This mapping layer is important because inconsistent naming can otherwise fragment the same biological or pharmacological concept across multiple records.

---

# ⚙️ Integrated Risk Engine

## Step 6 — Integrated Risk Prioritization

`06_Integrated_Risk_Engine.ipynb`

The final stage combines information from the experimental toxicity and pharmacovigilance pipelines.

Conceptually:

```text
             ┌──────────────────────┐
             │ Tox21 ML Prediction  │
             └──────────┬───────────┘
                        │
                        ▼
                 Molecular Evidence
                        │
                        │
                        ├──────────────┐
                        │              │
                        ▼              ▼
                 Model Confidence   SHAP Evidence
                        │              │
                        └──────┬───────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │ Integrated Engine  │
                    └─────────┬──────────┘
                              ▲
                              │
                    FAERS Signal Evidence
                              │
                              ▼
                    Pharmacovigilance Data

```

The integrated output is a **prioritization score** designed to help identify candidates that may deserve additional investigation.

It should **not** be interpreted as:

- A clinical probability
- A probability of an adverse event in an individual patient
- A causal effect estimate
- A regulatory safety determination

---

# 🏗️ Project Architecture

```text
                    ┌─────────────────┐
                    │   Tox21 Data    │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Molecular Features  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Toxicity ML Models  │
                  └──────────┬──────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
          Model Evaluation            SHAP/XAI
                 │                       │
                 └───────────┬───────────┘
                             │
                             ▼
                   ┌──────────────────┐
                   │ Integrated Risk  │
                   │     Engine       │
                   └────────┬─────────┘
                            ▲
                            │
                   ┌────────┴─────────┐
                   │      FAERS       │
                   └────────┬─────────┘
                            │
                            ▼
                   Signal Detection

```

---

# 📁 Project Structure

```text
ImmunoToxAI/
│
├── data/
│   ├── raw/
│   │   ├── tox21/
│   │   ├── faers/
│   │   └── drug_mapping/
│   │
│   ├── processed/
│   │   ├── tox21/
│   │   ├── faers/
│   │   └── integrated/
│   │
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
│   │
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

---

# 🚀 Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd ImmunoToxAI

python -m pip install -r requirements.txt

```

---

# ▶️ Running the Project

Run the notebooks in the following order:

```text
01_Tox21_EDA.ipynb
        ↓
02_Molecular_Features.ipynb
        ↓
03_Toxicity_Model.ipynb
        ↓
04_FAERS_EDA.ipynb
        ↓
05_AE_Signal_Detection.ipynb
        ↓
06_Integrated_Risk_Engine.ipynb

```

This order reflects the intended data-processing and modeling pipeline.

---

# 🖥️ Dashboard

The project includes a Streamlit dashboard for exploring model outputs and integrated risk information.

Run:

```bash
streamlit run dashboard/app.py
```

The dashboard is intended to make model and pharmacovigilance outputs easier to inspect without requiring users to work directly inside the notebooks.

---

# 🧪 Testing

Run the automated test suite with:

```bash
pytest -q
```

Tests cover core components such as:

* Data preprocessing
* Molecular feature generation
* FAERS signal calculations
* Risk-engine logic

---

# ⚙️ Configuration

Project parameters are separated from the source code through YAML configuration files:

```text
configs/
├── config.yaml
├── tox21.yaml
└── faers.yaml
```

This makes it easier to modify:

* Input paths
* Model parameters
* Thresholds
* Signal-detection settings
* Feature-processing options
* Risk-engine weights

without changing the core source code.

---

# 🛡️ Project Principles

ImmunoToxAI follows principles designed to make the analysis reproducible, interpretable, and scientifically responsible.

### Reproducibility

Data paths, configuration, preprocessing, and model settings are separated and documented to support reproducible experimentation.

### Leakage-Aware Modeling

Train/test separation and preprocessing are designed to reduce information leakage and provide more reliable evaluation.

### Scaffold-Aware Validation

Where molecular structure information permits, scaffold-aware validation can be used to provide a more realistic estimate of generalization to chemically distinct compounds.

### Appropriate Metrics

PR-AUC and other class-imbalance-aware metrics are emphasized rather than relying solely on accuracy.

### Probability Calibration

Selected models can be calibrated to improve the interpretation of predicted probabilities.

### Explainability

SHAP and other interpretation techniques are used to investigate model behavior and identify the features contributing to predictions.

### Transparent Pharmacovigilance

FAERS signal calculations are kept explicit rather than hidden inside an opaque risk score.

### Evidence Separation

The project explicitly distinguishes between different levels of computational evidence:

```text
Prediction ≠ Association ≠ Signal ≠ Causality
```

A model prediction or pharmacovigilance signal should not automatically be interpreted as evidence of causality.

### Human Review

Potentially important findings should be reviewed by qualified domain experts before being used for scientific, clinical, or regulatory decision-making.

---

# ⚠️ Limitations

## Tox21 Limitations

Tox21 provides valuable high-throughput experimental evidence, but it does not represent the complete biological complexity of human immunotoxicity.

Limitations include:

* Assay-specific endpoints
* In-vitro experimental conditions
* Limited representation of human physiology
* Missing or uncertain labels
* Class imbalance
* Potential distribution shift between training compounds and new compounds

Therefore, model predictions should be interpreted as **computational evidence**, not definitive biological conclusions.

---

## FAERS Limitations

FAERS is based primarily on spontaneous adverse-event reporting.

Important limitations include:

* Reporting bias
* Under-reporting
* Missing exposure denominators
* Confounding
* Duplicate or incomplete reports
* Changes in reporting behavior
* Differences in reporting rates across drugs and events

A statistically significant disproportionality signal does **not** establish that a drug caused the reported event.

---

## Integrated Risk Score Limitations

The integrated score combines multiple sources of evidence for **safety-signal prioritization**.

It is not:

```text
Clinical Risk Probability
        ≠
Causal Risk Estimate
        ≠
Regulatory Decision
```

The score should therefore be interpreted as a **prioritization mechanism for further investigation**, rather than a definitive measure of clinical or causal risk.

---

# 📈 Model Evaluation Philosophy

The project emphasizes scientific evaluation rather than simply obtaining the highest numerical score.

Important considerations include:

```text
Data Quality
     ↓
Leakage Prevention
     ↓
Appropriate Validation
     ↓
Class Imbalance
     ↓
Discrimination
     ↓
Calibration
     ↓
Interpretability
     ↓
Domain Review
```

A model with slightly lower discrimination but substantially better calibration or interpretability may be more useful for scientific investigation than a black-box model optimized for a single metric.

---

# 📚 Documentation

Additional technical documentation is available under:

```text
docs/
├── data_dictionary.md
├── methodology.md
├── model_card.md
└── limitations.md
```

These documents provide additional information about:

* Dataset fields
* Target definitions
* Modeling methodology
* Evaluation strategy
* Model limitations
* Intended use
* Risk considerations

---

# 🎯 Portfolio Positioning

ImmunoToxAI demonstrates an end-to-end applied machine-learning workflow for the biotech and pharmaceutical domain.

### Technical Skills Demonstrated

**Data Science**

* Python
* Pandas
* NumPy
* Exploratory Data Analysis
* Statistical analysis

**Machine Learning**

* Classification
* Ensemble models
* Multitask learning
* Imbalanced learning
* Probability calibration
* Model evaluation

**Explainable AI**

* SHAP
* Feature importance
* Model interpretation

**Cheminformatics**

* Molecular descriptors
* Molecular fingerprints
* Structure-derived features

**Pharmacovigilance**

* FAERS analysis
* Adverse-event analysis
* Disproportionality analysis
* Safety signal detection

**Data Engineering**

* Reproducible pipelines
* Configuration management
* Data preprocessing
* Dataset mapping

**Software Engineering**

* Modular Python source code
* Unit testing
* Configuration files
* Git/GitHub workflow

**Deployment**

* Streamlit
* Model artifacts
* Interactive risk exploration

---

# 🔬 Intended Use

ImmunoToxAI is intended for:

* Research and educational purposes
* Machine-learning portfolio demonstration
* Hypothesis generation
* Candidate safety prioritization
* Exploratory pharmacovigilance analysis
* Demonstration of explainable biotech ML workflows

It is **not intended for**:

* Clinical diagnosis
* Patient-level medical decisions
* Regulatory approval decisions
* Establishing drug-event causality
* Replacing toxicology or pharmacovigilance experts

---

# 🧠 Project Purpose & Philosophy

The goal of ImmunoToxAI is **not to claim that AI can determine whether a drug is safe or unsafe**.

Instead, the system is designed as an **AI-assisted pharmacovigilance and safety-analysis framework** that brings together molecular evidence, experimental toxicity data, and real-world adverse-event signals to identify potentially important safety patterns.

The core workflow is:

```text
Detect
  ↓
Quantify
  ↓
Explain
  ↓
Prioritize
  ↓
Investigate
```

### Detect

Identify potentially meaningful patterns across molecular, experimental, and adverse-event data.

### Quantify

Estimate the strength or relative importance of detected signals using machine-learning models and pharmacovigilance analytics.

### Explain

Provide interpretable evidence showing why a compound, drug, or safety signal was flagged.

### Prioritize

Use the available evidence to identify candidates that may warrant deeper scientific investigation.

### Investigate

Support researchers and domain experts in subsequent scientific evaluation rather than replacing their judgment.

### Example

If a particular drug is associated with an unusual increase in reports of a specific adverse event, ImmunoToxAI can:

1. Detect the potential safety pattern.
2. Quantify the strength of the signal.
3. Analyze the evidence contributing to the finding.
4. Prioritize the signal for further investigation.
5. Present the result for review by qualified researchers or safety professionals.

Importantly, the system does **not** conclude that the drug caused the adverse event.

Instead:

```text
Potential Pattern
       ↓
Computational Signal
       ↓
Evidence & Explanation
       ↓
Prioritization
       ↓
Expert Investigation
```

This distinction is central to the project:

> **AI can help surface potentially important safety signals earlier and make the evidence behind them easier to investigate. It should not be treated as a substitute for scientific, clinical, or regulatory judgment.**

---

# 📌 Key Takeaway

ImmunoToxAI connects heterogeneous safety evidence into a reproducible computational workflow:

```text
Molecular Evidence
        +
Experimental Toxicity
        +
Real-World Adverse Event Signals
        ↓
Machine Learning
        +
Pharmacovigilance Analytics
        +
Explainable AI
        ↓
Integrated Safety-Signal Prioritization
        ↓
Human / Domain-Expert Review
```

The practical objective is to **identify potentially important safety patterns earlier, explain the evidence behind them, and prioritize candidates for deeper scientific investigation**.

It is therefore best understood as an **AI-assisted safety-signal discovery and prioritization system**, rather than an automated system for determining whether a drug is safe or unsafe.
