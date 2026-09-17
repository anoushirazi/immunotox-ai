from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_class_balance(balance, path=None):
    fig, ax = plt.subplots(figsize=(11,6))
    sns.barplot(data=balance, x="positive_pct", y="endpoint", ax=ax)
    ax.set_xlabel("Positive class (%)")
    ax.set_ylabel("Endpoint")
    ax.set_title("Tox21 Endpoint Class Balance")
    fig.tight_layout()
    if path: fig.savefig(path, dpi=200, bbox_inches="tight")
    return fig

def plot_signal_volcano(signals, path=None):
    p = signals.copy()
    p = p[(p["PRR"] > 0) & p["p_value"].notna()].copy()
    p["logPRR"] = np.log2(p["PRR"].clip(lower=1e-9))
    p["neglog10p"] = -np.log10(p["p_value"].clip(lower=1e-300))
    fig, ax = plt.subplots(figsize=(11,7))
    sns.scatterplot(data=p.sample(min(len(p),10000), random_state=42),
                    x="logPRR", y="neglog10p", hue="evans_signal",
                    alpha=0.65, legend=False, ax=ax)
    ax.axvline(np.log2(2), linestyle="--")
    ax.set_title("FAERS Disproportionality Signals")
    fig.tight_layout()
    if path: fig.savefig(path, dpi=200, bbox_inches="tight")
    return fig
