# ImmunoToxAI Data Dictionary

## Tox21
- `mol_id`: molecule identifier.
- `smiles`: molecular structure.
- `NR-*`: nuclear-receptor assay endpoints.
- `SR-*`: stress-response assay endpoints.
- Endpoint values are binary assay labels with possible missing values.

## FAERS
- `report_id`: report identifier.
- `receive_date`, `year`, `month`, `quarter`: reporting time fields.
- `serious`, `is_fatal`, `is_hospitalized`, `is_life_threat`, `is_disabling`: seriousness indicators.
- `reactions`, `primary_reaction`: adverse-event terminology.
- `suspect_drug`, `brand_name`: drug identity fields.
- `pharm_class`: pharmacological class.
- Demographic and geographic fields provide contextual stratification.

## Derived fields
- `is_immune_related`: transparent keyword-based screening flag.
- `PRR`: proportional reporting ratio.
- `ROR`: reporting odds ratio.
- `chi2`: chi-squared statistic for the 2x2 table.
- `evans_signal`: screening flag using count >= 3, PRR >= 2, chi2 >= 4.
