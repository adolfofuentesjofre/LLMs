#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/source_data"
OUT = ROOT / "results/reproduced"


def main() -> None:
    grid = pd.read_csv(SOURCE / "adult_primary_v1/chile_model_grid_27_metrics.csv")
    cross = pd.read_csv(SOURCE / "crosscountry_treatment_balanced_model_summary.csv")
    anchors = pd.read_csv(SOURCE / "endpoint_anchor_diagnostic_summary.csv")
    if len(grid) != 27 or set(grid.n_uuids.astype(int)) != {1991}:
        raise RuntimeError("Chile grid is not the confirmed-adult 27-cell grid")
    rows = [
        ("chile_grid_conditions", len(grid)),
        ("chile_grid_participants", int(grid.n_uuids.iloc[0])),
        ("crosscountry_summary_rows", len(cross)),
        ("endpoint_anchor_summary_rows", len(anchors)),
        ("chile_min_variance_fraction_human", grid.variance_fraction_human.min()),
        ("chile_max_variance_fraction_human", grid.variance_fraction_human.max()),
        ("chile_min_human_agreement", grid.human_agreement.min()),
        ("chile_max_human_agreement", grid.human_agreement.max()),
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "headline_verification.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["quantity", "value"])
        writer.writerows(rows)
    print(OUT / "headline_verification.csv")


if __name__ == "__main__":
    main()
