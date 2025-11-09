from __future__ import annotations
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Any, List

REQUIRED_COLS = {"variant", "n", "conversions"}

@dataclass
class ExperimentRows:
    name: str
    hypothesis: str
    primary_metric: str
    metric_rows: List[Dict[str, int]]

def load_experiment_csv(path: str) -> ExperimentRows:
    df = pd.read_csv(path)
    cols = set(c.lower() for c in df.columns)
    if not REQUIRED_COLS.issubset(cols):
        raise ValueError(f"CSV must contain columns: {sorted(REQUIRED_COLS)} (got {sorted(cols)})")
    df = df.rename(columns={c: c.lower() for c in df.columns})
    if df.shape[0] < 2:
        raise ValueError("CSV needs at least two rows (A and B).")
    for _, r in df.iterrows():
        n, x = int(r["n"]), int(r["conversions"])
        if n < 0 or x < 0 or x > n:
            raise ValueError(f"Invalid row values n={n}, conversions={x}")
    def norm_variant(v: str) -> str:
        v = str(v).strip().lower()
        if v in {"a", "control", "baseline"}: return "control"
        if v in {"b", "treatment", "variant"}: return "treatment"
        return v
    df["variant"] = df["variant"].map(norm_variant)
    chosen = []
    for label in ["control", "treatment"]:
        part = df[df["variant"] == label]
        if not part.empty:
            chosen.append(part.iloc[0])
    if len(chosen) < 2:
        df_unique = df.drop_duplicates(subset=["variant"]).head(2)
        if df_unique.shape[0] < 2:
            raise ValueError("Could not identify two variants in CSV.")
        chosen = [df_unique.iloc[0], df_unique.iloc[1]]
    rows = []
    for r in chosen:
        rows.append({"variant": r["variant"], "n": int(r["n"]), "x": int(r["conversions"])})
    name_cols = [c for c in df.columns if c.lower()=="experiment_name"]
    hyp_cols = [c for c in df.columns if c.lower()=="hypothesis"]
    pm_cols  = [c for c in df.columns if c.lower()=="primary_metric"]
    name_val = df.iloc[0][name_cols[0]] if name_cols else "Untitled Experiment"
    hyp_val  = df.iloc[0][hyp_cols[0]] if hyp_cols else "(not provided)"
    pm_val   = df.iloc[0][pm_cols[0]]  if pm_cols  else "conversion_rate"
    return ExperimentRows(name=str(name_val), hypothesis=str(hyp_val), primary_metric=str(pm_val), metric_rows=rows)
