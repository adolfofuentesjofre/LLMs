from __future__ import annotations

import csv
from pathlib import Path


EXPECTED = {
    ("Chile", "C20 primary"): (1991, 20, 39820),
    ("France", "C20 primary"): (843, 20, 16860),
    ("Brazil", "C20 primary"): (434, 20, 8680),
    ("France", "C10 sensitivity"): (847, 10, 8470),
    ("Brazil", "C10 sensitivity"): (515, 10, 5150),
}


def validate_public_cohort_summary(path: Path) -> None:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    observed = {
        (row["country"], row["cohort"]): (
            int(row["participants"]),
            int(row["decisions_per_participant"]),
            int(row["decision_rows"]),
        )
        for row in rows
    }
    if observed != EXPECTED:
        raise RuntimeError(f"Confirmed-adult cohort mismatch: {observed}")
