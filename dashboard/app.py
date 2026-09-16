from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ImmunoToxAI",
    page_icon="🧬",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🧬 ImmunoToxAI")

st.caption(
    "Early drug-safety decision-support: Tox21 + FAERS"
)

st.info(
    "This dashboard is intended for R&D triage and hypothesis generation. "
    "It is not a clinical decision tool and does not establish causality."
)


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

signal_path = (
    ROOT
    / "data"
    / "processed"
    / "faers"
    / "faers_drug_ae_signals.parquet"
)

risk_path = (
    ROOT
    / "data"
    / "processed"
    / "integrated"
    / "drug_level_faers_risk.parquet"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_numeric(series):
    """Convert a pandas Series to numeric safely."""
    return pd.to_numeric(series, errors="coerce")


def finite_values(series):
    """
    Return only finite numeric values.
    Removes +inf, -inf and NaN.
    """
    values = safe_numeric(series)

    return values[
        values.notna()
        & values.replace(
            [float("inf"), float("-inf")],
            pd.NA
        ).notna()
    ]


def format_number(value, decimals=2):
    """Format numeric values safely for the dashboard."""
    if value is None:
        return "N/A"

    try:
        value = float(value)

        if value != value:
            return "N/A"

        if value == float("inf"):
            return "∞"

        if value == float("-inf"):
            return "-∞"

        return f"{value:,.{decimals}f}"

    except Exception:
        return "N/A"


def clean_display_dataframe(df):
    """
    Replace infinite numeric values with NA for cleaner
    Streamlit display.
    """
    display_df = df.copy()

    numeric_columns = display_df.select_dtypes(
        include="number"
    ).columns

    for col in numeric_columns:
        display_df[col] = display_df[col].replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

    return display_df


# ============================================================
# SECTION 1
# FAERS SIGNAL EXPLORER
# ============================================================

st.header("FAERS Signal Explorer")

if not signal_path.exists():

    st.warning(
        "FAERS signal file was not found. "
        "Run Notebook 05 or the FAERS signal pipeline first."
    )

else:

    # --------------------------------------------------------
    # LOAD SIGNAL DATA
    # --------------------------------------------------------

    try:
        signals = pd.read_parquet(signal_path)

    except Exception as e:

        st.error(
            f"Could not load the FAERS signal file:\n\n{e}"
        )

        st.stop()


    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if "suspect_drug" not in signals.columns:

        st.error(
            "The FAERS signal file does not contain "
            "the required 'suspect_drug' column."
        )

        st.stop()


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_term = st.text_input(
        "Drug name",
        value="",
        placeholder="Enter drug name, e.g. VALSARTAN",
    )


    # --------------------------------------------------------
    # FILTER DATA
    # --------------------------------------------------------

    if search_term.strip():

        view = signals[
            signals["suspect_drug"]
            .astype("string")
            .str.contains(
                search_term.strip(),
                case=False,
                na=False,
                regex=False,
            )
        ].copy()

    else:

        view = signals.copy()


    # ========================================================
    # FAERS OVERVIEW KPIs
    # ========================================================

    total_records = len(signals)

    displayed_records = len(view)

    unique_drugs = (
        signals["suspect_drug"]
        .dropna()
        .astype(str)
        .nunique()
    )


    if "ae" in signals.columns:

        unique_adverse_events = (
            signals["ae"]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        unique_adverse_events = 0


    st.subheader("FAERS Overview")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total records",
            f"{total_records:,}"
        )


    with col2:

        st.metric(
            "Displayed records",
            f"{displayed_records:,}"
        )


    with col3:

        st.metric(
            "Unique drugs",
            f"{unique_drugs:,}"
        )


    with col4:

        st.metric(
            "Unique adverse events",
            f"{unique_adverse_events:,}"
        )


    # --------------------------------------------------------
    # KPI EXPLANATION
    # --------------------------------------------------------

    with st.expander("What do these numbers mean?"):

        st.markdown(
            """
### Total records

The total number of records available in the loaded FAERS
signal dataset.

These are **drug–adverse-event signal records**, not necessarily
the number of individual patients.

### Displayed records

The number of records remaining after applying the
**Drug name** search filter.

If no drug name is entered, Displayed records equals
Total records.

### Unique drugs

The number of distinct drugs found in the
`suspect_drug` column.

### Unique adverse events

The number of distinct adverse-event terms found
in the `ae` column.

---

For example, if the dashboard shows:

- Total records = 447,383
- Displayed records = 447,383
- Unique drugs = 9,828
- Unique adverse events = 13,940

it means that the current FAERS signal dataset contains
447,383 drug–adverse-event records involving 9,828 unique
drugs and 13,940 unique adverse-event terms.
"""
        )


    # ========================================================
    # SIGNAL TABLE
    # ========================================================

    st.subheader("FAERS Signal Table")


    display_signals = view.copy()


    # Sort by Chi-square when available

    if "chi2" in display_signals.columns:

        display_signals["chi2"] = safe_numeric(
            display_signals["chi2"]
        )

        display_signals = display_signals.sort_values(
            "chi2",
            ascending=False,
            na_position="last",
        )


    # Limit display size

    display_signals = display_signals.head(200).copy()


    # Clean infinite values for visual display

    display_signals = clean_display_dataframe(
        display_signals
    )


    if display_signals.empty:

        st.warning(
            "No FAERS records were found for this drug."
        )

    else:

        st.caption(
            "Showing up to 200 records. "
            "Rows can be selected to inspect a drug."
        )


        # ----------------------------------------------------
        # ROW SELECTION
        # ----------------------------------------------------

        try:

            event = st.dataframe(
                display_signals,
                use_container_width=True,
                height=520,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="faers_signal_table",
            )

        except TypeError:

            # Compatibility fallback for older Streamlit versions

            st.dataframe(
                display_signals,
                use_container_width=True,
                height=520,
                hide_index=True,
            )

            event = None


    # ========================================================
    # DRUG SELECTION
    # ========================================================

    selected_drug = None


    # --------------------------------------------------------
    # Get drug from selected row
    # --------------------------------------------------------

    if event is not None:

        try:

            selected_rows = event.selection.rows

            if selected_rows:

                selected_index = selected_rows[0]

                if selected_index < len(display_signals):

                    selected_drug = display_signals.iloc[
                        selected_index
                    ]["suspect_drug"]

        except Exception:

            pass


    # --------------------------------------------------------
    # Alternative drug selector
    # --------------------------------------------------------

    drug_options = sorted(
        view["suspect_drug"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    if drug_options:

        selector_options = ["-- Select a drug --"] + drug_options

        selected_from_dropdown = st.selectbox(
            "Or select a drug to inspect",
            selector_options,
            index=0,
        )

        if selected_from_dropdown != "-- Select a drug --":

            selected_drug = selected_from_dropdown


    # ========================================================
    # DRUG DETAILS
    # ========================================================

    if selected_drug:

        st.divider()

        st.header(
            f"Drug Details — {selected_drug}"
        )


        # Get ALL signal records for selected drug

        drug_data = signals[
            signals["suspect_drug"]
            .astype(str)
            .str.upper()
            == str(selected_drug).upper()
        ].copy()


        # ----------------------------------------------------
        # Drug detail KPIs
        # ----------------------------------------------------

        signal_count = len(drug_data)


        if "PRR" in drug_data.columns:

            prr_values = finite_values(
                drug_data["PRR"]
            )

            max_prr = (
                prr_values.max()
                if not prr_values.empty
                else None
            )

        else:

            max_prr = None


        if "chi2" in drug_data.columns:

            chi_values = finite_values(
                drug_data["chi2"]
            )

            max_chi2 = (
                chi_values.max()
                if not chi_values.empty
                else None
            )

        else:

            max_chi2 = None


        if "ROR" in drug_data.columns:

            ror_values = finite_values(
                drug_data["ROR"]
            )

            max_ror = (
                ror_values.max()
                if not ror_values.empty
                else None
            )

        else:

            max_ror = None


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Signal count",
                f"{signal_count:,}"
            )


        with col2:

            st.metric(
                "Max PRR",
                format_number(max_prr)
            )


        with col3:

            st.metric(
                "Max ROR",
                format_number(max_ror)
            )


        with col4:

            st.metric(
                "Max Chi²",
                format_number(max_chi2)
            )


        # ----------------------------------------------------
        # Selected drug adverse events
        # ----------------------------------------------------

        st.subheader(
            "Adverse-event evidence"
        )


        if "ae" in drug_data.columns:

            ae_summary = (
                drug_data[
                    [
                        col
                        for col in [
                            "ae",
                            "PRR",
                            "ROR",
                            "chi2",
                            "p_value",
                            "a",
                            "b",
                            "c",
                            "d",
                        ]
                        if col in drug_data.columns
                    ]
                ]
                .copy()
            )


            if "chi2" in ae_summary.columns:

                ae_summary["chi2"] = safe_numeric(
                    ae_summary["chi2"]
                )

                ae_summary = ae_summary.sort_values(
                    "chi2",
                    ascending=False,
                    na_position="last",
                )


            ae_summary = clean_display_dataframe(
                ae_summary
            )


            st.dataframe(
                ae_summary.head(100),
                use_container_width=True,
                height=420,
                hide_index=True,
            )

        else:

            st.warning(
                "The signal dataset does not contain an 'ae' column."
            )


        # ----------------------------------------------------
        # Technical interpretation
        # ----------------------------------------------------

        with st.expander(
            "How should these FAERS metrics be interpreted?"
        ):

            st.markdown(
                """
**PRR (Proportional Reporting Ratio)**

Measures whether an adverse event is reported
proportionally more often with a drug compared with
other drugs in the dataset.

Higher values indicate stronger disproportionality.

**ROR (Reporting Odds Ratio)**

Another disproportionality measure based on the
2×2 contingency table.

**Chi²**

Measures the statistical departure from independence
between the drug and adverse event.

A very large Chi² can occur when the observed association
is highly different from the expected counts.

**p-value**

Provides a statistical measure associated with the
observed disproportionality under the model used by
the pipeline.

**a, b, c, d**

These represent the four cells of the 2×2 contingency
table used to calculate disproportionality statistics.

Important:

> FAERS disproportionality signals are useful for
> hypothesis generation and signal detection, but they
> do not by themselves establish causality.
"""
            )


# ============================================================
# SECTION 2
# DRUG-LEVEL RISK EVIDENCE
# ============================================================

st.divider()

st.header("Drug-level Risk Evidence")


if not risk_path.exists():

    st.warning(
        "Drug-level risk file was not found. "
        "Run the integrated FAERS risk pipeline first."
    )

else:

    # --------------------------------------------------------
    # LOAD RISK DATA
    # --------------------------------------------------------

    try:

        risk_df = pd.read_parquet(
            risk_path
        )

    except Exception as e:

        st.error(
            f"Could not load the risk file:\n\n{e}"
        )

        st.stop()


    # --------------------------------------------------------
    # Convert expected numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "max_prr",
        "max_chi2",
        "signal_count",
        "faers_strength",
        "faers_component",
        "seriousness_component",
        "risk_score",
    ]


    for col in numeric_columns:

        if col in risk_df.columns:

            risk_df[col] = safe_numeric(
                risk_df[col]
            )


    # ========================================================
    # RISK KPIs
    # ========================================================

    drugs_evaluated = len(risk_df)


    if "signal_count" in risk_df.columns:

        drugs_with_signals = (
            risk_df["signal_count"]
            .fillna(0)
            .gt(0)
            .sum()
        )

    else:

        drugs_with_signals = "N/A"


    # IMPORTANT:
    # Do not allow +inf PRR to dominate the KPI.

    if "max_prr" in risk_df.columns:

        finite_prr = finite_values(
            risk_df["max_prr"]
        )

        max_prr = (
            finite_prr.max()
            if not finite_prr.empty
            else None
        )

    else:

        max_prr = None


    if "max_chi2" in risk_df.columns:

        finite_chi2 = finite_values(
            risk_df["max_chi2"]
        )

        max_chi2 = (
            finite_chi2.max()
            if not finite_chi2.empty
            else None
        )

    else:

        max_chi2 = None


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Drugs evaluated",
            f"{drugs_evaluated:,}"
        )


    with col2:

        if isinstance(
            drugs_with_signals,
            int
        ):

            st.metric(
                "Drugs with signals",
                f"{drugs_with_signals:,}"
            )

        else:

            st.metric(
                "Drugs with signals",
                drugs_with_signals
            )


    with col3:

        st.metric(
            "Maximum PRR",
            format_number(max_prr)
        )


    with col4:

        st.metric(
            "Maximum Chi²",
            format_number(max_chi2)
        )


    # --------------------------------------------------------
    # PRR infinity warning
    # --------------------------------------------------------

    if "max_prr" in risk_df.columns:

        inf_prr_count = (
            risk_df["max_prr"]
            .isin([
                float("inf"),
                float("-inf")
            ])
            .sum()
        )

        if inf_prr_count > 0:

            st.warning(
                f"{inf_prr_count:,} drug records contain "
                "an infinite PRR value. "
                "This can occur when the denominator of "
                "the PRR calculation is zero. "
                "Infinite PRR values are excluded from "
                "the Maximum PRR KPI."
            )


    # ========================================================
    # RISK METRIC EXPLANATION
    # ========================================================

    with st.expander(
        "Explanation of Drug-level Risk Evidence"
    ):

        st.markdown(
            """
### max_prr

The maximum PRR observed for a drug across its
associated adverse events.

A high value indicates strong disproportionality.

An infinite PRR can occur when the denominator of
the PRR equation becomes zero. This should be treated
carefully rather than interpreted as an infinitely strong
clinical risk.

### max_chi2

The maximum Chi-square statistic observed for the drug.

Higher values indicate stronger statistical
departure from independence.

### signal_count

The number of FAERS drug–adverse-event signals
associated with the drug.

### faers_strength

A component of the existing FAERS-based risk model
generated by the project's pipeline.

### faers_component

The FAERS contribution used by the integrated
risk framework.

### seriousness_component

A component representing seriousness information
used by the existing risk model.

### risk_score

The final integrated drug-level risk score produced
by the existing pipeline.

**Important:** The dashboard does not modify or
recalculate the existing risk_score formula.

The purpose here is to display, explore and prioritize
the output of the established pipeline.
"""
        )


    # ========================================================
    # RISK TABLE
    # ========================================================

    st.subheader(
        "Drug-level Risk Ranking"
    )


    # --------------------------------------------------------
    # Optional drug filter
    # --------------------------------------------------------

    risk_search = st.text_input(
        "Filter risk table by drug",
        value="",
        placeholder="Enter drug name...",
    )


    risk_view = risk_df.copy()


    if risk_search.strip():

        if "suspect_drug" in risk_view.columns:

            risk_view = risk_view[
                risk_view["suspect_drug"]
                .astype("string")
                .str.contains(
                    risk_search.strip(),
                    case=False,
                    na=False,
                    regex=False,
                )
            ].copy()


    # --------------------------------------------------------
    # Sort by risk_score
    # --------------------------------------------------------

    if "risk_score" in risk_view.columns:

        risk_view = risk_view.sort_values(
            "risk_score",
            ascending=False,
            na_position="last",
        )

    elif "max_chi2" in risk_view.columns:

        risk_view = risk_view.sort_values(
            "max_chi2",
            ascending=False,
            na_position="last",
        )


    # Show top 100

    risk_display = risk_view.head(100).copy()


    risk_display = clean_display_dataframe(
        risk_display
    )


    st.caption(
        "Risk ranking is sorted by the existing risk_score "
        "when available."
    )


    st.dataframe(
        risk_display,
        use_container_width=True,
        height=520,
        hide_index=True,
    )


    # ========================================================
    # RISK DISTRIBUTION
    # ========================================================

    st.subheader(
        "Risk Signal Distribution"
    )


    if (
        "max_prr" in risk_df.columns
        and "max_chi2" in risk_df.columns
    ):

        plot_df = risk_df[
            [
                "max_prr",
                "max_chi2",
            ]
        ].copy()


        plot_df["max_prr"] = safe_numeric(
            plot_df["max_prr"]
        )

        plot_df["max_chi2"] = safe_numeric(
            plot_df["max_chi2"]
        )


        # Remove invalid / infinite values

        plot_df = plot_df[
            plot_df["max_prr"].notna()
            & plot_df["max_chi2"].notna()
        ]


        plot_df = plot_df[
            plot_df["max_prr"].replace(
                [float("inf"), float("-inf")],
                pd.NA,
            ).notna()
        ]


        plot_df = plot_df[
            plot_df["max_chi2"].replace(
                [float("inf"), float("-inf")],
                pd.NA,
            ).notna()
        ]


        if not plot_df.empty:

            st.scatter_chart(
                plot_df,
                x="max_prr",
                y="max_chi2",
                use_container_width=True,
            )

            st.caption(
                "Each point represents a drug. "
                "The plot shows the relationship between "
                "maximum PRR and maximum Chi-square."
            )

        else:

            st.info(
                "Not enough finite PRR/Chi² values are available "
                "to generate the visualization."
            )


    # ========================================================
    # DATA DISTRIBUTION SUMMARY
    # ========================================================

    with st.expander(
        "Statistical summary of risk metrics"
    ):

        summary_data = {}


        if "max_prr" in risk_df.columns:

            finite_prr = finite_values(
                risk_df["max_prr"]
            )

            if not finite_prr.empty:

                summary_data["Median max PRR"] = (
                    finite_prr.median()
                )

                summary_data["95th percentile max PRR"] = (
                    finite_prr.quantile(0.95)
                )


        if "max_chi2" in risk_df.columns:

            finite_chi2 = finite_values(
                risk_df["max_chi2"]
            )

            if not finite_chi2.empty:

                summary_data["Median max Chi²"] = (
                    finite_chi2.median()
                )

                summary_data["95th percentile max Chi²"] = (
                    finite_chi2.quantile(0.95)
                )


        if summary_data:

            summary_df = pd.DataFrame(
                {
                    "Metric": summary_data.keys(),
                    "Value": [
                        format_number(v)
                        for v in summary_data.values()
                    ],
                }
            )

            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No finite risk metrics are available."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ImmunoToxAI | Tox21 + FAERS | "
    "Early drug-safety decision support for R&D triage"
)