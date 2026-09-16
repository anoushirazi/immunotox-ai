# ImmunoToxAI Model Card

## Intended use
Early R&D safety triage, candidate prioritization, assay follow-up prioritization, and pharmacovigilance hypothesis generation.

## Models
- Endpoint-specific Random Forest classifiers for Tox21.
- Classical FAERS disproportionality calculations for drug–AE pairs.
- Transparent weighted risk engine.

## Outputs
- Tox21 endpoint probabilities.
- FAERS PRR/ROR/chi-squared signals.
- Integrated risk-prioritization score.

## Limitations
Tox21 assays are pathway-level proxies; FAERS is a spontaneous-reporting database without a reliable exposure denominator and is subject to confounding and reporting bias. The integrated score is not validated for clinical or regulatory decision-making.
